from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from kokoro.pipeline import KPipeline
import torch
import numpy as np
import io
import soundfile as sf
from django.http import HttpResponse

# Initialize Kokoro TTS at startup
try:
    tts_pipeline = KPipeline(lang_code="a")  # 'a' for American English
    print("✅ Kokoro TTS model loaded successfully.")
except Exception as e:
    tts_pipeline = None
    print(f"❌ Error loading Kokoro TTS model: {e}")

class TextToSpeechView(APIView):
    def get(self, request, *args, **kwargs):
        text = request.query_params.get("text", "").strip()
        voice = request.query_params.get("voice", "af_heart")
        return self.process_tts(text, voice)

    def post(self, request, *args, **kwargs):
        text = request.data.get("text", "").strip()
        voice = request.data.get("voice", "af_heart")
        return self.process_tts(text, voice)

    def process_tts(self, text, voice):
        if not text:
            return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Generate audio from text
            audio_result = list(tts_pipeline(text, voice=voice))[0]
            audio_numpy = audio_result.output.audio.detach().cpu().numpy()

            # Convert to in-memory buffer instead of saving a file
            audio_buffer = io.BytesIO()
            sf.write(audio_buffer, audio_numpy, samplerate=22050, format="WAV")
            audio_buffer.seek(0)  # Reset buffer position

            # Return audio as an HTTP response
            response = HttpResponse(audio_buffer, content_type="audio/wav")
            response["Content-Disposition"] = 'inline; filename="output.wav"'
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from rest_framework.views import APIView
from rest_framework.response import Response
import speech_recognition as sr

class SpeechToTextAPI(APIView):
    def post(self, request):
        action = request.data.get("action")

        if action == "start":
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("🎤 Listening... Speak now!")
                audio = recognizer.listen(source)  # User manually starts talking
            
            try:
                text = recognizer.recognize_google(audio)
                return Response({"text": text})
            except sr.UnknownValueError:
                return Response({"error": "Could not understand the audio"})
            except sr.RequestError as e:
                return Response({"error": f"API request error: {e}"})

        return Response({"error": "Invalid action. Send {'action': 'start'} in POST request."}, status=400)
