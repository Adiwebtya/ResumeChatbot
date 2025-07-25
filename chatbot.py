import os
import logging
from dotenv import load_dotenv

import PyPDF2

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from prompt import QUESTION_PROMPT_TEMPLATE, ATS_PASSABILITY_PROMPT

load_dotenv()

# === CONFIG ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Please set the GROQ_API_KEY environment variable.")
GROQ_MODEL = "llama3-8b-8192"

from config import CHROMA_DB_PATH


class ResumeChatbot:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.resume_text = ""
        self.vector_db = None
        self.retriever = None

        # Embeddings & LLM
        self.embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
            max_tokens=512,
            temperature=0.7
        )

    def extract_text(self):
        pdf_reader = PyPDF2.PdfReader(self.pdf_path)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
        self.resume_text = text.strip()
        logger.info(f"✅ Extracted {len(self.resume_text)} characters from PDF.")
        return self.resume_text

    def split_text(self):
        if not self.resume_text:
            raise ValueError("No resume text to split. Did you run extract_text()?")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_text(self.resume_text)
        logger.info(f"✅ Split text into {len(chunks)} chunks.")
        return chunks

    def create_vector_store(self, chunks):
        documents = [Document(page_content=chunk) for chunk in chunks]
        self.vector_db = Chroma.from_documents(
            documents,
            self.embedder,
            persist_directory=CHROMA_DB_PATH
        )
        logger.info(f"✅ Vector store created with {len(documents)} documents.")
        self.retriever = self.vector_db.as_retriever(search_kwargs={"k": 5})

    def load_vector_store(self):
        self.vector_db = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=self.embedder
        )
        self.retriever = self.vector_db.as_retriever(search_kwargs={"k": 5})
        logger.info(f"✅ Loaded vector store from {CHROMA_DB_PATH}.")

    def get_context(self, question: str):
        if not self.retriever:
            raise ValueError("Vector store not loaded. Call load_vector_store() or create_vector_store() first.")
        docs = self.retriever.invoke(question)
        context = "\n\n".join([doc.page_content for doc in docs])
        logger.info(f"✅ Retrieved {len(docs)} relevant chunks for the question.")
        return context

    def ask_question(self, question: str):
        context = self.get_context(question)
        prompt = QUESTION_PROMPT_TEMPLATE.format(
            context=context,
            question=question
        )
        response = self.llm.invoke(prompt)
        return response.content.strip()

    def ats_passability_score_llm(self):
        prompt = ATS_PASSABILITY_PROMPT.format(
            resume=self.resume_text
        )
        response = self.llm.invoke(prompt)
        return response.content.strip()