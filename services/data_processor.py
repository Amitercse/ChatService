from flask import jsonify, Response, json
from services.gemini_model_configure import get_gemini_model

def process_message_logic(message: str) -> Response:
    try:
        # Generate content using the Gemini model
        # The 'generate_content' method sends the prompt to the model
        model = get_gemini_model()
        prompt = message + " output the response in json array of objects that can be returned from application as json REST response"
        response = model.generate_content(prompt)

        # Access the generated text from the response
        generated_text = response.text

        return json.loads(generated_text.strip())

    except Exception as e:
        # Catch any errors during the API call and return an error message
        print(f"Error generating content: {e}")
        return jsonify({"error": f"Failed to generate content: {str(e)}"}), 500