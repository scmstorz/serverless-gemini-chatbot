import functions_framework
import os
import json
from flask import Request, make_response, jsonify

# --- Vertex AI / Gemini ---
import vertexai
from vertexai.generative_models import GenerativeModel, Part 

# --- Configuration ---
PROJECT_ID = os.environ.get("GCP_PROJECT")
LOCATION = os.environ.get("FUNCTION_REGION")
MODEL_ID = "gemini-2.0-flash" 

STATIC_CONTEXT = """
Put context and information the chabot should use here.
"""

# Initialize Vertex AI once globally (reduces cold starts)
try:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    # Pass the static context when creating the model object
    model = GenerativeModel(
        MODEL_ID,
        system_instruction=STATIC_CONTEXT
    )
    print(f"Vertex AI initialized successfully for project {PROJECT_ID} in {LOCATION} using model {MODEL_ID} with system instruction.")
except Exception as e:
    print(f"ERROR initializing Vertex AI: {e}")
    model = None

# --- Cloud Function Entry Point ---
@functions_framework.http
def handle_chat_proxy(request: Request):
    """
    HTTP Cloud Function proxy to Gemini API.
    Expects JSON: {"prompt": "user message"}
    Returns JSON: {"response": "gemini response"}
    System instruction is set during model initialization.
    """
    # Set CORS headers for preflight request
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # Set CORS headers for main request
    cors_headers = {
        'Access-Control-Allow-Origin': '*'
    }

    # Check method
    if request.method != 'POST':
        return make_response(jsonify(error='Method Not Allowed'), 405, cors_headers)

    # Check model initialization
    if model is None:
         print("ERROR: Vertex AI Model not initialized.")
         return make_response(jsonify(error='Internal Server Error: Model not initialized'), 500, cors_headers)

    # Get JSON data
    try:
        request_json = request.get_json(silent=True)
        if not request_json or 'prompt' not in request_json:
            raise ValueError("Invalid JSON payload or missing 'prompt' key.")
        user_prompt = request_json['prompt']
        if not user_prompt:
             raise ValueError("'prompt' cannot be empty.")
    except ValueError as e:
        print(f"ERROR: Bad Request - {e}")
        return make_response(jsonify(error=f"Bad Request: {e}"), 400, cors_headers)
    except Exception as e:
        print(f"ERROR parsing request JSON: {e}")
        return make_response(jsonify(error='Bad Request: Could not parse JSON'), 400, cors_headers)

    print(f"Received prompt: {user_prompt}")

    # Call the Gemini API
    try:
        generation_config = {
            "max_output_tokens": 2048,
            "temperature": 1,
            "top_p": 1,
        }
        safety_settings = {} # Define if needed

        print(f"Sending prompt to Gemini model ({MODEL_ID})... (System instruction applied during init)")

        response = model.generate_content(
            [user_prompt], # Pass prompt as a list
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=False,
        )

        print("Received response from Gemini.")

        # Extract the text response (slightly improved error check)
        llm_response_text = ""
        try:
             # Using .text directly is often sufficient and simpler if available
             llm_response_text = response.text
        except ValueError as ve:
             # Handle cases where the response was blocked (often raises ValueError)
             print(f"WARN: Could not extract text directly, likely blocked. Response: {response}")
             # You could inspect response.candidates[0].finish_reason here if needed
             llm_response_text = "I cannot provide a response to that request due to safety or other restrictions."
        except Exception as extraction_error:
             print(f"ERROR extracting text from response: {extraction_error}")
             llm_response_text = "There was an issue processing the response."


        print(f"LLM Response: {llm_response_text}")

        # Return the response as JSON
        return make_response(jsonify(response=llm_response_text), 200, cors_headers)

    except Exception as e:
        print(f"ERROR calling Gemini API: {e}")
        # import traceback
        # print(traceback.format_exc()) # Uncomment for detailed debugging if needed
        return make_response(jsonify(error=f"Internal Server Error: Failed to get response from LLM - {e}"), 500, cors_headers)


