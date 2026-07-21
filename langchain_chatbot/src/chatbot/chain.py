from operator import itemgetter

from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda

from src.chatbot.prompt import prompt
import httpx

def format_docs(docs):

    formatted = []

    for doc in docs:

        text = f"""
            Section: {doc.metadata.get('section')}

            Subsection: {doc.metadata.get('subsection')}

            Content:
            {doc.page_content}
            """

        formatted.append(text)

    return "\n\n".join(formatted)


def build_chain(retriever):

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        http_client=httpx.Client(verify=False, timeout=30.0),
    )

    # Retrieve docs once and keep them alongside the question
    setup = RunnableParallel(
        question=RunnablePassthrough(),
        docs=retriever
    )

    # Generate LLM answer AND pass through the source documents
    answer_and_sources = RunnableParallel(
        answer=(
            RunnableLambda(lambda x: {"context": format_docs(x["docs"]), "question": x["question"]})
            | prompt
            | llm
            | StrOutputParser()
        ),
        source_documents=itemgetter("docs")
    )

    chain = setup | answer_and_sources

    return chain