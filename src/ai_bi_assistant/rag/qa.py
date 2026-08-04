from langchain_core.prompts import ChatPromptTemplate

from ai_bi_assistant.agents.llm import llm
from ai_bi_assistant.rag.retriever import retrieve_documents


prompt = ChatPromptTemplate.from_template(
"""
You are a Spotify business analyst.

Answer ONLY using the supplied context.

If the answer is not present, say:

"I couldn't find this information in the uploaded reports."

Context:

{context}

Question:

{question}
"""
)

chain = prompt | llm


def answer_question(question: str):

    docs = retrieve_documents(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    response = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    return response.content