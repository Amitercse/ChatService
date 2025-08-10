from typing import Any, Coroutine

from flask import jsonify
from services.rag_handler import user_input

async def process_message_logic(message: str) -> Coroutine[Any, Any, Any]:
    try:
        generated_text = await user_input(message)
        return generated_text

    except Exception as e:
        print(f"Error processing message: {e}")
        return jsonify({"error": f"Failed to process message: {str(e)}"}), 500