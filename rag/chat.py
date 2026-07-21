from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
embedding_model=HuggingFaceEmbeddings(
  model_name="BAAI/bge-small-en-v1.5"
)

client=OpenAI(
  api_key=os.getenv("api_key"),
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


vector_db=QdrantVectorStore.from_existing_collection(
  url="http://localhost:6333",
  collection_name="learning_rag",
  embedding=embedding_model,
)

#Now take the user input

user_query=input("Ask something:")

#Returns the relevant chunks 
search_results=vector_db.similarity_search(query=user_query)

context = "\n\n\n".join(
    [
        f"Page Content: {result.page_content}\n"
        f"Page Number: {result.metadata['page_label']}\n"
        f"File Location: {result.metadata['source']}"
        for result in search_results
    ]
)

SYSTEM_PROMPT="""
  You are a helpful AI assistant who answers user query based on the available context retrived from a PDF file along with 
  page_contents and page number.
  
  You should only answer the user based on the following context and navigate the user to open the right page number to know more.
  
  Context:
  {context}
  
"""

response=client.chat.completions.create(
 model="gemini-3.1-flash-lite",
 messages=[
   {"role":"system","content":SYSTEM_PROMPT},
   {"role":"user","content":user_query}
 ] 
)

print(f"{response.choices[0].message.content}")