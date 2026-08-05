import os
import shutil
import requests

from dotenv import load_dotenv

from langchain_core.embeddings import Embeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


class JinaEmbeddings(Embeddings):
    def __init__(self):
        self.api_key = os.getenv("JINA_API_KEY")
        self.url = "https://api.jina.ai/v1/embeddings"
        self.model = "jina-embeddings-v3"

    def embed_documents(self, texts):
        embeddings = []

        print(f"\nCreating embeddings for {len(texts)} chunks...\n")

        for i, text in enumerate(texts):

            response = requests.post(
                self.url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "input": text,
                },
                timeout=60,
            )

            response.raise_for_status()

            embeddings.append(
                response.json()["data"][0]["embedding"]
            )

            if (i + 1) % 25 == 0:
                print(f"✓ {i + 1}/{len(texts)} chunks embedded")

        print("\nFinished creating embeddings.\n")

        return embeddings

    def embed_query(self, text):

        response = requests.post(
            self.url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "input": text,
            },
            timeout=60,
        )

        response.raise_for_status()

        return response.json()["data"][0]["embedding"]


def ingest_documents():

    print("=" * 70)
    print("RAG DOCUMENT INGESTION")
    print("=" * 70)

    pdf_folder = "documents"

    if not os.path.exists(pdf_folder):
        print(f"Folder '{pdf_folder}' not found.")
        return

    documents = []

    print("\nLoading PDFs...\n")

    for file in os.listdir(pdf_folder):

        if file.lower().endswith(".pdf"):

            print(f"Reading: {file}")

            loader = PyPDFLoader(
                os.path.join(pdf_folder, file)
            )

            docs = loader.load()

            print(f"Loaded {len(docs)} pages.")

            documents.extend(docs)

    if not documents:
        print("No PDF documents found.")
        return

    print(f"\nTotal pages loaded: {len(documents)}")

    print("\nSplitting documents...\n")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=250,
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    embeddings = JinaEmbeddings()

    if os.path.exists("chroma_db"):
        print("\nRemoving old Chroma database...")
        shutil.rmtree("chroma_db")

    print("\nCreating new Chroma database...\n")

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db",
    )

    print("\n" + "=" * 70)
    print("VECTOR DATABASE CREATED SUCCESSFULLY")
    print("=" * 70)
    print(f"Chunks stored : {len(chunks)}")
    print(f"Location      : {os.path.abspath('chroma_db')}")
    print("=" * 70)


if __name__ == "__main__":
    ingest_documents()