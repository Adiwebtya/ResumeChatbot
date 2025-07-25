
from chatbot import ResumeChatbot

if __name__ == "__main__":
    pdf_path = "super_final_resume.pdf"
    chatbot = ResumeChatbot(pdf_path)

    chatbot.extract_text()
    chunks = chatbot.split_text()

    # First run: create the store
    chatbot.create_vector_store(chunks)

    # Later runs: load the store
    chatbot.load_vector_store()

    while True:
        option = input("\nType 'ask' to ask a question or 'ats' to check ATS score: ").strip().lower()

        if option == 'ask':
            question = input("What do you want to know? ")
            answer = chatbot.ask_question(question)
            print("\n=== ✅ Answer ===\n")
            print(answer)

        elif option == 'ats':
            feedback = chatbot.ats_passability_score_llm()
            print("\n=== 📌 ATS Passability Report ===\n")
            print(feedback)
