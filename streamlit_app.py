import streamlit as st
from chatbot import ResumeChatbot

st.set_page_config(page_title="Resume Chatbot", page_icon="🤖", layout="wide")

st.title("🤖 Resume Chatbot")
st.write("Upload your resume PDF below, then ask questions or check ATS passability score!")

uploaded_file = st.file_uploader("📄 Upload your Resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ Resume uploaded. Processing...")

    chatbot = ResumeChatbot("temp_resume.pdf")

    # Do everything automatically in the background
    extracted_text = chatbot.extract_text()
    chunks = chatbot.split_text()
    chatbot.create_vector_store(chunks)

    st.success("✅ Resume processed and ready!")

    question = st.text_input("❓ Ask a question about your resume:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💬 Get Answer"):
            if question.strip() == "":
                st.warning("Please enter a question.")
            else:
                answer = chatbot.ask_question(question)
                st.info(f"**Answer:** {answer}")

    with col2:
        if st.button("✅ Get ATS Passability Score"):
            score = chatbot.ats_passability_score_llm()
            st.success("ATS Passability Score:")
            st.write(score)
