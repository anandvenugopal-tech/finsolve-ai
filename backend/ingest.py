import sys

try:
    import pwd
except ImportError:
    import magic
    import os
    # Create a dummy module for Windows
    from types import ModuleType
    mock_pwd = ModuleType("pwd")
    sys.modules["pwd"] = mock_pwd

from langchain_community.document_loaders import (
    TextLoader,UnstructuredMarkdownLoader, PyPDFLoader, CSVLoader)
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os 
    
departments = ['finance', 'hr', 'marketing', 'engineering', 'general']

def load_documents(dept: str):
    docs = []
    folder_path = f"data/{dept}"

    for file in os.listdir(folder_path):
                if file.endswith(".md"):
                    loader = UnstructuredMarkdownLoader(os.path.join(folder_path, file), encoding = 'utf-8')
                elif file.endswith(".pdf"):
                    loader = PyPDFLoader(os.path.join(folder_path, file), encoding = 'utf-8')
                elif file.endswith(".csv"):
                    loader = CSVLoader(os.path.join(folder_path, file), encoding = 'utf-8')
                else:
                    loader = TextLoader(os.path.join(folder_path, file), encoding = 'utf-8')

                documents = loader.load()
                
                for doc in documents:
                    doc.metadata = {'department': dept}
                    doc.metadata = {'source': file}
                docs.extend(documents)

    return docs

def ingest_all():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

    for dept in departments:
        print(f"Ingesting: {dept}")
        raw_docs = load_documents(dept)
        chunks = splitter.split_documents(raw_docs)

        Chroma.from_documents(
             chunks,
             embeddings,
             collection_name=f"dept_{dept}",
             persist_directory = './chroma_db'
        )

        print(f" -> {len(chunks)}")


if __name__ == "__main__":
     ingest_all()

