from flask import Flask, render_template, request, jsonify, session
from chatbot import UniversityChatbot
from email_sender import send_chat_email

app = Flask(__name__)

app.secret_key = "university_secret_key"

bot = UniversityChatbot()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/save-student-info", methods=["POST"])
def save_student_info():
    data = request.json

    session["student_info"] = {
        "name": data.get("name"),
        "email": data.get("email"),
        "contact": data.get("contact"),
        "department": data.get("department")
    }

    session["chat_history"] = []

    return jsonify({"success": True})


@app.route("/get-response", methods=["POST"])
def get_response():
    user_message = request.json.get("message")
    personality = request.json.get("personality", "general")

    if not user_message:
        return jsonify({"response": "Please type a question."})

    if "chat_history" not in session:
        session["chat_history"] = []

    session["chat_history"].append({
        "role": "user",
        "content": user_message
    })

    bot_response = bot.get_response(
        user_message,
        session["chat_history"],
        personality
    )

    session["chat_history"].append({
        "role": "assistant",
        "content": bot_response
    })

    session["last_personality"] = personality

    return jsonify({"response": bot_response})


@app.route("/end-chat", methods=["POST"])
def end_chat():
    student_info = session.get("student_info")
    chat_history = session.get("chat_history", [])
    personality = session.get("last_personality", "general")

    if session.get("email_sent"):
        return jsonify({
            "success": True,
            "message": "Chat session already sent."
        })

    if not student_info:
        return jsonify({"success": False, "message": "Student info not found."})

    if not chat_history:
        return jsonify({"success": False, "message": "No chat history found."})

    try:
        send_chat_email(student_info, chat_history, personality)

        session["email_sent"] = True

        return jsonify({
            "success": True,
            "message": "Chat session sent successfully to the concerned department."
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Email sending failed: {str(e)}"
        })

if __name__ == "__main__":
    app.run(debug=True)