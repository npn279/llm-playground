import os
import logging
import dotenv
dotenv.load_dotenv()

from openai import OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def generate(**kwargs):
    try:
        model = kwargs.get('model', 'gpt-3.5-turbo')
        temperature = kwargs.get('temperature', 0.9)
        system_prompt = kwargs.get('system_prompt', 'You are a helpful assistant.')
        max_tokens = kwargs.get('max_tokens', 500)
        stream = kwargs.get('stream', False)
        messages = kwargs.get('messages', [{"role": "assistant", "content": system_prompt}, {"role": "user", "content": "Hello!"}])

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
        )

        return response
    except Exception as e:
        logging.error(f"Error generating text: {e}")
        return None

