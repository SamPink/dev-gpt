from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import ReadTheDocsLoader
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
import pickle

# load .env file
from dotenv import load_dotenv

load_dotenv()

from langchain.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://python.langchain.com/en/latest/")
raw_documents = loader.load()

""" # Load Data
loader = ReadTheDocsLoader("langchain.readthedocs.io")
raw_documents = loader.load() """

# Split text
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(raw_documents)


# Load Data to vectorstore
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)


# Save vectorstore
with open("vectorstore.pkl", "wb") as f:
    pickle.dump(vectorstore, f)

import pickle
from query_data import get_chain

# load .env file
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    with open("vectorstore.pkl", "rb") as f:
        vectorstore = pickle.load(f)
    qa_chain = get_chain(vectorstore)
    chat_history = []
    print("Chat with your docs!")
    while True:
        print("Human:")
        question = input()
        result = qa_chain({"question": question, "chat_history": chat_history})
        chat_history.append((question, result["answer"]))
        print("AI:")
        print(result["answer"])
