import os
from rest_framework.response import Response
from rest_framework.views import APIView
from transformers import AutoTokenizer
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate

def chatbot_page(request):
    print("hello")

# Load API token from environment variable
huggingfacehub_api_token = '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'
if not huggingfacehub_api_token:
    raise ValueError("Hugging Face API token not found. Please set the HUGGINGFACEHUB_API_TOKEN environment variable.")

# Initialize model and tokenizer
model_name = "HuggingFaceH4/starchat-beta"
tokenizer = AutoTokenizer.from_pretrained(model_name)

llm = HuggingFaceHub(
    repo_id=model_name,
    huggingfacehub_api_token=huggingfacehub_api_token,
    model_kwargs={
        "min_length": 10,
        "max_new_tokens": 50,  # You can lower this if needed
        "do_sample": True,
        "temperature": 0.2,
        "top_k": 50,
        "top_p": 0.95,
        "eos_token_id": 49155,
    },
)

# Limit to the last 5 chat messages to avoid exceeding token limits
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    return_messages=True,
    k=5  # Keep only the most recent 5 exchanges
)

prompt_template = PromptTemplate(
    input_variables=["chat_history", "input"],
    template="{chat_history}\nYou: {input}\nAI:"
)

llm_chain = LLMChain(
    prompt=prompt_template,
    llm=llm,
    memory=memory,
)

class ChatbotAPIView(APIView):
    """
    API endpoint for chatbot communication
    """
    def post(self, request):
        user_input = request.data.get("message", "")
        if not user_input.strip():
            return Response({"error": "Empty message"}, status=400)

        try:
            raw_reply = llm_chain.predict(input=user_input)
            reply = raw_reply.split("AI:")[-1].strip() if "AI:" in raw_reply else raw_reply.strip()
            return Response({"response": reply})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
