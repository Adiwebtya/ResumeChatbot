# prompts.py

QUESTION_PROMPT_TEMPLATE = """
You are a helpful assistant. Use the context below to answer the question clearly and concisely.

Context:
\"\"\"
{context}
\"\"\"

Question: {question}

Answer:
"""

ATS_FEEDBACK_PROMPT_TEMPLATE = """
You are an ATS (Applicant Tracking System) assistant.

Below is a resume and a job description.
The calculated match score is: {ats_score}%

Your tasks:
1️⃣ Explain how well this resume matches the job.
2️⃣ List any missing important keywords or skills.
3️⃣ Suggest 3–5 clear improvements to increase the match score.

=== RESUME ===
{resume}

=== JOB DESCRIPTION ===
{job_description}

=== ATS SCORE ===
{ats_score}%

Your detailed feedback:
"""


ATS_PASSABILITY_PROMPT = """
You are an expert ATS (Applicant Tracking System) advisor.

Below is a resume.  
Your task is to analyze it and estimate an ATS Passability Score from 0% to 100%.

Please check:
✅ If the resume uses a clear, standard format.  
✅ Whether it’s easily machine-readable (no images instead of text).  
✅ Whether standard sections like Experience, Education, Skills are present and labeled clearly.  
✅ Whether the text uses simple fonts and no unusual characters.  
✅ If the length is reasonable (1–2 pages).

Then:
1️⃣ Give your estimated ATS Passability Score (%).  
2️⃣ Explain any formatting issues that could hurt parsing.  
3️⃣ Suggest 3–5 improvements to make it fully ATS-friendly.

=== RESUME START ===
{resume}
=== RESUME END ===

Your response must start with:
ATS Score: XX%

Then your explanation and suggestions.
"""
