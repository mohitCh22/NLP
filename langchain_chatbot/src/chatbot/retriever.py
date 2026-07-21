def get_retriever(vectorstore):

    # retriever = vectorstore.as_retriever(
    #     search_type="similarity",
    #     search_kwargs={"k": 4}
    # )
    retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 4,
        "fetch_k": 10
        }
    )

    return retriever