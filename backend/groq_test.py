import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = PromptTemplate.from_template("Summarize this in one sentence: {text}")
model = ChatGroq(model="openai/gpt-oss-20b")
parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({"text": "LangGraph lets you build stateful, multi-step LLM workflows as graphs."})
print(result)