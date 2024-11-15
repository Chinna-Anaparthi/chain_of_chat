from fastapi import FastAPI, HTTPException, Form
from vertexai.generative_models import GenerativeModel
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"serverKey.json"

app = FastAPI()

# Initialize chat session and history globally
chat_session = None

# Function to generate the response
def get_gemini_response(user_prompt: str):
    global chat_session
    try:
        if chat_session is None:
            model = GenerativeModel(model_name="gemini-1.5-pro-002", system_instruction="system instruction")
            chat_session = model.start_chat()

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "max_output_tokens": 8192,
        }

        final_result = ""
        prompt = f"User's original request: {user_prompt}"

        response = chat_session.send_message(prompt, generation_config=generation_config)
        final_result = response.text  # Keep updating with the latest output
            

        print("final_result:", final_result)
        return final_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")

# API endpoint for processing the user prompt
@app.post("/generate_response/")
async def generate_response(user_prompt: str = Form(...)):
    try:
        response_text = get_gemini_response(user_prompt)
        return {"response": response_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7000)
