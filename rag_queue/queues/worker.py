from openai import OpenAI
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
import os

embedding_model=HuggingFaceEmbeddings(
  model_name="BAAI/bge-small-en-v1.5"
)

vector_db=QdrantVectorStore.from_existing_collection(
  url="http://localhost:6333",
  collection_name="learning_rag",
  embedding=embedding_model,
)

load_dotenv()


client=OpenAI(
  api_key=os.getenv("api_key"),
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
def process_query(query:str):
  print("Searching chunks",query)
  searchResults=vector_db.similarity_search(query=query)
  context = "\n\n\n".join(
    [
        f"Page Content: {result.page_content}\n"
        f"Page Number: {result.metadata['page_label']}\n"
        f"File Location: {result.metadata['source']}"
        for result in searchResults
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
        {"role":"system","content":SYSTEM_PROMPT.format(context=context)},
        {"role":"user","content":query}
      ] 
    )
  return response.choices[0].message.content
  