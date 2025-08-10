from flask import Blueprint, request, jsonify
from services.data_processor import process_message_logic

# Create a Blueprint for chat-related routes
# The url_prefix='/chat' means all routes defined in this blueprint
# will be prefixed with /chat (e.g., /chat/process)
chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

@chat_bp.route('/process', methods=['POST'])
async def process_data():
    """
    Handles POST requests to the /chat/process endpoint.
    It expects a JSON payload with a 'message' field.
    The service will process this message by calling a separate business logic function
    and return a JSON response.
    """
    # Use a try-except block for robust error handling
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        if 'message' not in data:
            return jsonify({"error": "Missing 'message' field in JSON data"}), 400

        # Extract the message from the JSON data
        user_message = data['message']

        # --- Call Business Logic ---
        processed_message = await process_message_logic(user_message)

        # Check if the result is a tuple (an error response from the logic function)
        if isinstance(processed_message, tuple):
            return processed_message

        # Prepare the response data as a dictionary
        response_data = {
            "original_message": user_message,
            "processed_message": processed_message,
            "status": "success"
        }

        # Return the JSON response with a 200 OK status code
        return jsonify(response_data), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        # Return a 500 Internal Server Error for unhandled exceptions
        return jsonify({"error": "An internal server error occurred", "details": str(e)}), 500
