from langchain_openai import ChatOpenAI
import os

def get_model(model_name: str):
    return ChatOpenAI(model_name=model_name, temperature=0, api_key=os.getenv("OPENAI_API_KEY"))