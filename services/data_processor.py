from flask import jsonify, Response, json
import google.generativeai as genai

GEMINI_API_KEY = "your_api_key"
# Configure the generative AI model
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Initialize the Gemini model
    # You can choose different models like 'gemini-pro', 'gemini-pro-vision', etc.
    model = genai.GenerativeModel(model_name='gemini-2.0-flash',
                                  generation_config={
                                      "response_mime_type": "application/json", # Tell the model to output JSON
                                  })
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    print("Please ensure your GEMINI_API_KEY is correctly set.")
    model = None # Set model to None to indicate failure


def process_message_logic(message: str) -> Response:
    try:
        # Generate content using the Gemini model
        # The 'generate_content' method sends the prompt to the model
        prompt = message + " output the response in json array of objects that can be returned from application as json REST response"
        response = model.generate_content(prompt)

        # Access the generated text from the response
        generated_text = response.text
        print(repr(generated_text))

        return json.loads(generated_text.strip())

    except Exception as e:
        # Catch any errors during the API call and return an error message
        print(f"Error generating content: {e}")
        return jsonify({"error": f"Failed to generate content: {str(e)}"}), 500