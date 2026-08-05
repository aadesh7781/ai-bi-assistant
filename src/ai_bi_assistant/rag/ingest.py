import os

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma

from langchain_openai import OpenAIEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


def ingest_documents():
    """
    Load PDFs, split them into chunks, create embeddings,
    and store them inside a Chroma vector database.
    """

    print("=" * 60)
    print("RAG DOCUMENT INGESTION")
    print("=" * 60)

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

            documents.extend(loader.load())

    if len(documents) == 0:
        print("No PDF documents found.")
        return

    print(f"\nLoaded {len(documents)} pages.")

    print("\nSplitting documents...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    print("\nConnecting to Jina AI...")

    embeddings = OpenAIEmbeddings(
        api_key=os.getenv("JINA_API_KEY"),
        base_url="https://api.jina.ai/v1",
        model="jina-embeddings-v3",
    )

    print("Creating Chroma vector database...")

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db",
    )

    print("\n✅ Vector database created successfully!")

    print(f"Stored {len(chunks)} chunks.")

    print(f"Location: {os.path.abspath('chroma_db')}")


if __name__ == "__main__":
    ingest_documents()