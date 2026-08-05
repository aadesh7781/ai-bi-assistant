from ai_bi_assistant.rag.retriever import retrieve_documents


def test(query):
    print("\n" + "=" * 80)
    print("QUERY:", query)
    print("=" * 80)

    docs = retrieve_documents(query, k=5)

    print(f"\nRetrieved {len(docs)} documents.\n")

    for i, doc in enumerate(docs, 1):
        print("=" * 80)
        print(f"DOCUMENT {i}")
        print("=" * 80)
        print(doc.page_content[:1200])
        print()


if __name__ == "__main__":

    test("AI strategy")

    test("artificial intelligence")

    test("machine learning")

    test("generative AI")

    test("Spotify AI")