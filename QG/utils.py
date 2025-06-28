import io
import re
import json
import tempfile
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from .models import MCQQuestion

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

AZURE_ENDPOINT = "https://aimodels9077570365.services.ai.azure.com/models"
AZURE_API_KEY = "DnFRR9q9019T9r28cI5v1jAGnswPo0ODN1nBctwScn2CRxjhvbs0JQQJ99BEACF24PCXJ3w3AAAAACOGPyST"
AZURE_MODEL_NAME = "DeepSeek-V3-0324"

client = ChatCompletionsClient(
    endpoint=AZURE_ENDPOINT,
    credential=AzureKeyCredential(AZURE_API_KEY),
)

PROMPT_TEMPLATE = """
You are an expert assistant specializing in educational question generation.  
Generate at least **20 multiple-choice questions (MCQs)** based on the provided content.  
Strict guidelines:  
- Questions must come directly from the document content.  
- Each question must have **4 distinct answer choices (A, B, C, D)**.  
- Label the correct answer as **"correct_answer"**.  
- **Return only valid JSON output**.  

Context (Document Content):  
{context_text}  

Expected Output (Valid JSON Format Only):  

```json
[
  {{
    "question": "Example question?",
    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
    "correct_answer": "B) Option 2" # Ensure this is always provided
  }}
]
``` 
"""

def clean_text(text):
    return re.sub(r'\s+', ' ', text.replace("\n", " ").replace("\r", " ")).strip()

def load_pdf(file_bytes):
    # Save file bytes to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(file_bytes)  # Write bytes directly
        temp_pdf_path = temp_pdf.name  # Get the file path

    # Load the PDF using PDFPlumberLoader
    document_loader = PDFPlumberLoader(temp_pdf_path)
    docs = document_loader.load()

    return docs

def filter_pages(raw_documents):
    return [doc for doc in raw_documents if len(doc.page_content.strip()) > 100]

def adaptive_split(raw_documents):
    total_length = sum(len(doc.page_content) for doc in raw_documents)
    chunk_size = min(2000, max(500, total_length // 20))
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=200, add_start_index=True)
    return splitter.split_documents(raw_documents)

def extract_questions(text):
    matches = re.findall(r'\{\s*"question".*?\}', text, re.DOTALL)
    questions = []
    for match in matches:
        try:
            question_data = json.loads(match)
            questions.append({
                "question_text": question_data.get("question", ""),
                "options": question_data.get("options", []),
                "correct_answer": question_data.get("correct_answer", "")
            })
        except json.JSONDecodeError:
            continue
    return questions


def generate_questions_from_document(document_chunks):
    selected_chunks = document_chunks[:5]
    context_text = clean_text("\n\n".join([doc.page_content for doc in selected_chunks]))

    prompt = PROMPT_TEMPLATE.replace("{context_text}", context_text)

    response = client.complete(
        messages=[
            SystemMessage(content="You are an expert assistant specializing in educational question generation."),
            UserMessage(content=prompt)
        ],
        max_tokens=4096,
        temperature=0.3,
        top_p=0.9,
        presence_penalty=0.0,
        frequency_penalty=0.0,
        model=AZURE_MODEL_NAME
    )

    return response.choices[0].message.content



def generate_additional_questions(existing_questions, document_chunks):
    while len(existing_questions) < 13:  # Ensure at least 13 questions
        response = generate_questions_from_document(document_chunks)
        new_questions = extract_questions(response)

        # Ensure new questions are unique before adding
        for q in new_questions:
            if q not in existing_questions:
                existing_questions.append(q)



def generate_mcqs_from_pdf(file_bytes, file_name, document_index, course_name, course_id):
    raw_docs = load_pdf(file_bytes)
    filtered_docs = filter_pages(raw_docs)
    processed_chunks = adaptive_split(filtered_docs)

    # Generate initial questions
    response = generate_questions_from_document(processed_chunks)
    questions = extract_questions(response)

    # Ensure at least 13 questions
    if len(questions) < 13:
        generate_additional_questions(questions, processed_chunks)

    # Save questions to the database
    saved_questions = []
    for q in questions:
        options = q.get("options", [])

        # Ensure we have 4 options
        while len(options) < 4:
            options.append("N/A")

        correct_answer = q.get("correct_answer", "").strip() or "N/A"

        mcq = MCQQuestion.objects.create(
            document_index=document_index,
            course_name=course_name,
            course_id=course_id,  
            document_name=file_name,
            question_text=q["question_text"],
            option_a=options[0],
            option_b=options[1],
            option_c=options[2],
            option_d=options[3],
            correct_answer=correct_answer
        )

        saved_questions.append({
            "document_index": document_index,
            "course_name": course_name,
            "question_text": q["question_text"],
            "options": options,
            "correct_answer": correct_answer
        })

    return saved_questions