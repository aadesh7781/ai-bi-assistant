from ai_bi_assistant.rag.retriever import retrieve_documents


def test(query, k=5):

    print("\n" + "=" * 100)
    print(f"QUERY: {query}")
    print("=" * 100)

    docs = retrieve_documents(query, k=k)

    print(f"\nRetrieved {len(docs)} documents.\n")

    if not docs:
        print("No documents found.")
        return

    for i, doc in enumerate(docs, 1):

        print("=" * 100)
        print(f"DOCUMENT {i}")
        print("=" * 100)

        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "Unknown")

        print(f"Source : {source}")
        print(f"Page   : {page}")
        print("-" * 100)

        print(doc.page_content[:2000])
        print()


if __name__ == "__main__":

    queries = [
        "Compare our revenue with Spotify's reported revenue",
       
        
    ]

    for q in queries:
        test(q)