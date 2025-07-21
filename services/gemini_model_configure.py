import google.generativeai as genai

GEMINI_API_KEY = "your-gemini-key"

def get_gemini_model():
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

    return model
