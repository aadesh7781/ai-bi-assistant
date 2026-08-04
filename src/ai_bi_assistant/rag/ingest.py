import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


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
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    print("\nLoading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Creating Chroma vector database...")

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db",
    )

    print("\nVector database created successfully!")

    print(f"Location: {os.path.abspath('chroma_db')}")


if __name__ == "__main__":
    ingest_documents()