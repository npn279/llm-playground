import os
import logging
import dotenv
dotenv.load_dotenv()

import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate(**kwargs):
    try:
        model = kwargs.get('model', 'gemini-1.0-pro')
        temperature = kwargs.get('temperature', 0.9)
        max_tokens = kwargs.get('max_tokens', 500)
        # system_prompt = kwargs.get('system_prompt', 'You are a helpful assistant.')
        messages = kwargs.get('messages', [{"role": "assistant", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}])
        stream = kwargs.get('stream', False)
        # Set up the model
        generation_config = {
            "temperature": temperature,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": max_tokens,
        }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        ]

        model = genai.GenerativeModel(model_name=model,
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        prompt_parts = []
        for message in messages:
            prompt_parts.append(message['content'])

        response = model.generate_content(prompt_parts, stream=stream)
        return response

    except Exception as e:
        logging.error(f"Error generating text: {e}")
        return None