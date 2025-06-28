import whisper
import ffmpeg
import numpy as np
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
import re
import json

def extract_audio_to_numpy(video_path):
    out, _ = (
        ffmpeg
        .input(video_path)
        .output('pipe:', format='f32le', acodec='pcm_f32le', ac=1, ar='16000')
        .run(capture_stdout=True, capture_stderr=True)
    )
    audio = np.frombuffer(out, np.float32)
    return audio

def transcribe_video_in_memory(video_path):
    model = whisper.load_model("base")
    audio = extract_audio_to_numpy(video_path)
    result = model.transcribe(audio, fp16=False)
    return result

def filter_segments(segments):
    return [
        {
            'id': segment['id'],
            'start': segment['start'],
            'end': segment['end'],
            'text': segment['text']
        }
        for segment in segments
    ]

def chooseMoments(segments, number_of_images):
    AZURE_ENDPOINT = "https://aimodels9077570365.services.ai.azure.com/models"
    AZURE_API_KEY = "DnFRR9q9019T9r28cI5v1jAGnswPo0ODN1nBctwScn2CRxjhvbs0JQQJ99BEACF24PCXJ3w3AAAAACOGPyST"
    AZURE_MODEL_NAME = "DeepSeek-V3-0324"

    client = ChatCompletionsClient(
        endpoint=AZURE_ENDPOINT,
        credential=AzureKeyCredential(AZURE_API_KEY),
    )

    prompt = f"""You are given a list of video transcript segments, each with a start time, end time, and the spoken text. Your task is to analyze the content of each segment and select the best {number_of_images} moments where an image could be generated to visually represent the idea, scene, or concept being discussed.

Please return a list of the most {number_of_images} visually descriptive or conceptually rich segments where generating an image would enhance understanding or engagement. 

For each selected segment, provide:
_The id of the segment.
_The text of the segment.
_The start time of the segment.
_The end time of the segment.
_A suggestion Prompt for what the image should be, contain or look like.

Use the following list of segments:
{segments}
"""

    result = client.complete(
        model=AZURE_MODEL_NAME,
        messages=[
            SystemMessage(content="You are an expert multimedia content creator helping convert educational videos into engaging visual formats."),
            UserMessage(content=prompt)
        ],
        max_tokens=1024,
        temperature=0.7,
    )

    return result.choices[0].message.content

def extract_json_from_string(text, result):
    match = re.search(r"```json\s*(\[.*?\])\s*```", text, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            x = json.loads(json_str)
            x.append({'text': result['text']})
            return x
        except json.JSONDecodeError as e:
            raise ValueError(f"Found JSON block but failed to parse it: {e}")
    else:
        raise ValueError("No JSON array found in the input text.")

def overlay_image_on_video(video_path, img, start_time, end_time):
    from moviepy.video.io.VideoFileClip import VideoFileClip
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
    from moviepy.video.VideoClip import ImageClip
    from PIL import Image

    video = VideoFileClip(video_path)
    duration = video.duration

    if start_time >= end_time or end_time > duration:
        raise ValueError("Invalid time range.")

    aspect_ratio = img.width / img.height
    new_height = video.h
    new_width = int(aspect_ratio * new_height)
    resized_img = img.resize((new_width, new_height))
    resized_img_path = "resized_overlay_temp.png"
    resized_img.save(resized_img_path)

    image = ImageClip(resized_img_path)
    image.start = start_time
    image.end = end_time
    image.pos = lambda t: ((video.w - image.w) // 2, (video.h - image.h) // 2)

    final_video = CompositeVideoClip([video, image])
    return final_video

def GenerateImagesFromPrompts(BestMoments, video_path, number_of_images=1):
    from diffusers import DiffusionPipeline
    from moviepy.video.io.VideoFileClip import VideoFileClip
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
    from moviepy.video.VideoClip import ImageClip
    from PIL import Image

    video = VideoFileClip(video_path)
    pipe = DiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")

    clips = [video]

    for moment in BestMoments:
        if len(moment) < 4 or 'image_suggestion' not in moment:
            continue

        prompt = moment['image_suggestion']
        img = pipe(prompt).images[0]

        aspect_ratio = img.width / img.height
        new_height = video.h
        new_width = int(aspect_ratio * new_height)
        resized_img = img.resize((new_width, new_height))
        resized_img_path = "resized_overlay_temp.png"
        resized_img.save(resized_img_path)

        image = ImageClip(resized_img_path)
        image.start = moment['start']
        image.end = moment['end']
        image.pos = lambda t: ((video.w - image.w) // 2, (video.h - image.h) // 2)

        clips.append(image)
        print(f"✅ Overlayed image on video for moment {moment['id']}")

    final = CompositeVideoClip(clips)
    return final, clips

def main(video_file, number_of_images=2):
    result = transcribe_video_in_memory(video_file)
    segments = filter_segments(result['segments'])
    print("✅ Transcription and filtering done.")

    x = chooseMoments(segments, number_of_images)
    BestMoments = extract_json_from_string(x, result)

    print("✅ Best moments identified. Generating visuals and overlaying...")
    final_video, clips = GenerateImagesFromPrompts(BestMoments, video_file, number_of_images)

    print("✅ Video ready with visual overlays.")
    return final_video, clips
