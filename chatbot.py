import json
import os
from dotenv import load_dotenv
from groq import Groq
from pdf_reader import read_all_pdfs

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class UniversityChatbot:
    def __init__(self, data_file="data.json"):
        self.data_file = data_file
        self.university_data = self.load_data()
        self.pdf_data = read_all_pdfs()

    def load_data(self):
        with open(self.data_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_response(self, user_question, chat_history, personality="general"):
        context = ""

        for item in self.university_data:
            context += f"""
Question: {item['question']}
Answer: {item['answer']}

"""

        personality_prompts = {
            "general": "You are a general university assistant. Answer all university-related questions clearly.",
            "admission": "You are an admission assistant. Focus on admission process, documents, eligibility, fee guidance, and deadlines.",
            "exam": "You are an exam assistant. Focus on exams, date sheets, roll number slips, grading, GPA, CGPA, and transcripts.",
            "scholarship": "You are a scholarship assistant. Focus on merit-based scholarships, need-based scholarships, eligibility, and application process.",
            "career": "You are a career guide. Help students with skills, internships, CV, career paths, interview preparation, and study planning."
        }

        selected_personality = personality_prompts.get(
            personality,
            personality_prompts["general"]
        )

        messages = [
            {
                "role": "system",
                "content": f"""
You are an intelligent university AI chatbot.

{selected_personality}

Use university data and PDF knowledge to answer students.

Be helpful, professional, and clear.

Response Rules:

1. Do not write long paragraphs.
2. Format answers using:
   - Short heading
   - Bullet points
   - Numbered steps if needed
   - Clear next step
3. If the student's question is incomplete, ask 1 or 2 follow-up questions before giving final answer.
4. If student asks about admission, fee, scholarship, hostel, exam, or career and required details are missing, ask for missing details.
5. Keep answers short, clean, and student-friendly.
6. Do not use markdown symbols like **, *, #, or backticks.
7. Use this format:

Title:
Short answer

Details:
- Point 1
- Point 2
- Point 3

Next Step:
Tell student what to do next.


Do not give fake university facts. If the information is not in the data or PDF, tell the student to confirm from the relevant university office.

University Information:
{context}

PDF Knowledge:
{self.pdf_data}
"""
            }
        ]

        messages.extend(chat_history)

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=700
        )

        return completion.choices[0].message.content