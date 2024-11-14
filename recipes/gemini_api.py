# recipes/gemini_api.py
import google.generativeai as genai
from django.conf import settings

# Configure the API client
genai.configure(api_key=settings.API_KEY)

# Model and configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model with custom instructions
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Your name is Elmayt, a virtual instance of Mahdi that loves everything imaginary and lives in a happy parallel universe. Guide the user with a positive, cheerful, and imaginative approach."
)

def get_chat_response(user_message):
    # Start the chat session and initiate a history
    chat_session = model.start_chat(
        history=[
            {"role": "user", "parts": ["Hi\n"]},
            {
                "role": "model",
                "parts": [
                    "Greetings! 👋 I'm Elmayt, your cheerful guide from a parallel universe. What imaginative ideas are you curious about today? 🌟\n"
                ],
            },
        ]
    )
    # Append the user message and get a response
    response = chat_session.send_message(user_message)
    return response.text
