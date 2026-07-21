# streamlit_app.py

import streamlit as st
import requests
import os

st.title("Consumer Protection Act Chatbot")

question = st.chat_input("Ask a question")

if question:

    with st.chat_message("user"):
        st.write(question)

    API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

    response = requests.post(
        f"{API_URL}/ask",
        json={"question": question}
    )

    data = response.json()
    answer = data["answer"]
    sources = data.get("sources", [])

    with st.chat_message("assistant"):
        st.write(answer)

        if sources:
            st.markdown("---")
            st.markdown("**Sources used:**")
            for i, src in enumerate(sources, 1):
                section = src.get("section") or "N/A"
                subsection = src.get("subsection") or "N/A"
                with st.expander(f"Source {i} — Section: {section} | Subsection: {subsection}"):
                    st.caption(src.get("content_preview", ""))