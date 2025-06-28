from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import MCQQuestion
from .serializers import MCQQuestionSerializer
from .utils import generate_mcqs_from_pdf
import random
import os
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import QuizResult

class MCQGenerationView(APIView):
    def post(self, request):
        print("Received FILES:", request.FILES)  # Debugging

        if 'course_pdfs' not in request.FILES:
            return Response({"error": "No PDFs uploaded"}, status=400)

        uploaded_files = request.FILES.getlist('course_pdfs')
        
        if not uploaded_files:
            return Response({"error": "No PDFs uploaded"}, status=400)

        # Get course_id from request data
        course_id = request.data.get("course_id")
        if not course_id:
            return Response({"error": "course_id is required"}, status=400)

        try:
            course_id = int(course_id)
        except ValueError:
            return Response({"error": "course_id must be an integer"}, status=400)

        results = []
        for index, pdf_file in enumerate(uploaded_files, start=1):
            document_index = f"Lec{index}"
            filename_without_ext = os.path.splitext(pdf_file.name)[0]
            course_name = filename_without_ext

            file_bytes = pdf_file.read()
            print(f"Processing file: {pdf_file.name} | Course name: {course_name}")

            questions = generate_mcqs_from_pdf(
                file_bytes, 
                pdf_file.name, 
                document_index, 
                course_name, 
                course_id
            )
            results.append(questions)

        return Response(results, status=200)




class MCQListView(APIView):
    def get(self, request, *args, **kwargs):
        questions = MCQQuestion.objects.all()
        serializer = MCQQuestionSerializer(questions, many=True)
        return Response(serializer.data)
    
    
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_list_or_404
from .models import MCQQuestion
import random


def distribute_questions(weighted_dict, total_questions=20):
    total_weight = sum(weighted_dict.values()) or 1
    allocated = {k: max(2, min(18, round((v / total_weight) * total_questions))) for k, v in weighted_dict.items()}
    diff = total_questions - sum(allocated.values())
    keys = sorted(weighted_dict, key=weighted_dict.get, reverse=True)
    for _ in range(abs(diff)):
        for k in keys:
            if (diff > 0 and allocated[k] < 18) or (diff < 0 and allocated[k] > 2):
                allocated[k] += 1 if diff > 0 else -1
                diff += 1 if diff < 0 else -1
                if diff == 0:
                    break
    return allocated

def final_distribution(all_quizzes, numLec, prev_in=True, *degrees):
    num_quizzes = len(all_quizzes)
    
    if len(degrees) + 1 < numLec:
        return f'Out of scope, I just have {len(all_quizzes)} quizzes. Provide me with the material to help you.'
    elif not prev_in:
        return all_quizzes.get(f'Lec{numLec}', {})
    else:
        keys = list(all_quizzes.keys())
        if len(keys) == 2:
            return {k: 10 for k in keys}

        scores = {}
        quiz_keys = keys[:-1]  # All except the last one
        for key, degree in zip(quiz_keys, degrees):
            scores[key] = abs((degree / 2) - 9.5)

        distribution = distribute_questions(scores, total_questions=20 - 9)  # Reserve 9 for last lecture
        last_key = keys[-1]
        distribution[last_key] = 9
        return distribution



def miniquiz(quiz, numQues):
    return random.sample(quiz, min(numQues, len(quiz)))

def collection(dictionary, all_quizzes):
    final = {}
    for lec, numQues in dictionary.items():
        final[lec] = miniquiz(all_quizzes.get(lec, []), numQues)
    return final

def get_lecture_scores(lectures, course_id):
    # Get averages from the database
    results = (
        QuizResult.objects
        .filter(course=course_id, session__in=lectures)
        .values('session')
        .annotate(avg_score=Avg('score'))
    )
    print("Results from database:", list(results))  # Debug

    # Convert to a dictionary: { "Lec1": 8.5, "Lec3": 6.25 }
    score_dict = {item['session']: round(item['avg_score'] or 0, 2) for item in results}

    # Return list in same order as lectures
    return [score_dict.get(lec, 0.0) for lec in lectures]



class GenerateQuizAPIView(APIView):
    def post(self, request):
        data = request.data
        index = data.get("index")
        courseID = data.get("course_id")
        
        lectures = [f"Lec{i+1}" for i in range(index)]
        degrees = get_lecture_scores(lectures, courseID)
        
        print("Received lectures:", lectures)
        print("Received degrees:", degrees)

        if not lectures or not degrees or len(lectures) != len(degrees):
            return Response({"error": "Invalid input format"}, status=400)

        # Step 1: Create weighted dictionary
        weighted_dict = dict(zip(lectures, degrees))
        print("weighted_dict:", weighted_dict)
        question_distribution = final_distribution(weighted_dict, len(lectures), True, *degrees)
        print("question_distribution:", question_distribution)

        if isinstance(question_distribution, str):  # Handle errors from final_distribution
            return Response({"error": question_distribution}, status=400)

        # Step 2: Fetch questions from the database
        all_quizzes = {}
        for lecture in lectures:
            questions = get_list_or_404(MCQQuestion, document_index=lecture)
            all_quizzes[lecture] = [
                {
                    "question_text": q.question_text,
                    "options": [q.option_a, q.option_b, q.option_c, q.option_d],
                    "correct_answer": q.correct_answer,
                }
                for q in questions
            ]
        # Step 3: Generate final quiz
        final_quiz = collection(question_distribution, all_quizzes)
        
        return Response(final_quiz, status=200)
    
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# ✅ Azure configuration (fixed endpoint)
AZURE_ENDPOINT = "https://aimodels9077570365.services.ai.azure.com/models"
AZURE_API_KEY = "DnFRR9q9019T9r28cI5v1jAGnswPo0ODN1nBctwScn2CRxjhvbs0JQQJ99BEACF24PCXJ3w3AAAAACOGPyST"
AZURE_MODEL_NAME = "DeepSeek-V3-0324"  # ✅ this must be the *deployment name*

# ✅ Correct client instantiation
client = ChatCompletionsClient(
    endpoint=AZURE_ENDPOINT,
    credential=AzureKeyCredential(AZURE_API_KEY),
)

class GenerateReportView(APIView):
    def post(self, request):
        user = request.data.get("user")
        quiz = request.data.get("quiz")
        session_names = request.data.get("session", [])
        course = request.data.get("course")
        scores = request.data.get("score", [])

        # Validate input
        if not all([user, quiz, session_names, course, scores]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(session_names, list) or not isinstance(scores, list) or len(session_names) != len(scores):
            return Response({"error": "Session and score must be lists of equal length."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # ✅ Save each session-score pair to the database
            for session_name, score_value in zip(session_names, scores):
                QuizResult.objects.update_or_create(
                    user=user,
                    quiz=quiz,
                    session=session_name,
                    defaults={
                        "course": course,
                        "score": score_value
                    }
                )

            # Prepare data for report
            scores_dict = {session_name: score_value for session_name, score_value in zip(session_names, scores)}

            # Prompt construction
            prompt = f"""
You are an expert educational assistant. Your task is to generate a detailed student performance report based on their exam scores.

### **Instructions:**  
- Analyze the student's performance in each exam.  
- Identify strengths and weaknesses based on the scores.  
- Provide insights on areas that need improvement.  
- Suggest study strategies for better performance in future exams.  
- Keep the report structured, clear, and professional.  

### **Student Exam Scores:**  
{scores_dict}  

### **Expected Report Output:**  
1. **Overall Performance Summary:**  
   - Mention the student's strongest and weakest subjects.  
   - Compare their performance across different subjects.  

2. **Subject-Wise Analysis:**  
   - For each subject, provide a brief evaluation.  
   - If the score is above 85, praise their strong understanding.  
   - If the score is between 60-85, suggest improvement strategies.  
   - If the score is below 60, highlight urgent areas to work on.  

3. **Actionable Recommendations:**  
   - Suggest learning techniques (e.g., practice tests, revision strategies).  
   - Recommend specific resources (e.g., books, online courses).  
   - Encourage time management tips for exam preparation.  

Now, generate a **personalized performance report** based on the provided scores.
"""

            result = client.complete(
                model=AZURE_MODEL_NAME,
                messages=[
                    SystemMessage(content="You are a helpful assistant."),
                    UserMessage(content=prompt)
                ],
                max_tokens=1024,
                temperature=0.7,
            )

            generated_text = result.choices[0].message.content.strip()

            return Response({"report": generated_text}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)