import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


DEPARTMENT_EMAILS = {
    "general": "atiqworkhub@gmail.com",
    "admission": "atiqworkhub@gmail.com",
    "exam": "atiqworkhub@gmail.com",
    "scholarship": "atiqworkhub@gmail.com",
    "career": "atiqworkhub@gmail.com"
}


def send_chat_email(student_info, chat_history, personality):
    sender_email = os.getenv("MAIL_USERNAME")
    sender_password = os.getenv("MAIL_PASSWORD")

    receiver_email = DEPARTMENT_EMAILS.get(
        personality,
        DEPARTMENT_EMAILS["general"]
    )

    chat_text = ""

    for msg in chat_history:
        role = msg["role"].capitalize()
        content = msg["content"]
        chat_text += f"{role}: {content}\n\n"

    email_body = f"""
New University Chatbot Session

Student Details:
Name: {student_info.get("name")}
Email: {student_info.get("email")}
Contact: {student_info.get("contact")}
Department: {student_info.get("department")}

Selected Category:
{personality}

Chat History:
{chat_text}
"""

    msg = EmailMessage()
    msg["Subject"] = "New Student Chatbot Session"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(email_body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)