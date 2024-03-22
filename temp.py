from core import llm_gemini


msgs = [{"role": "system", "content": "Answer in vietnamese"}, {"role": "user", "content": "Hello!"}]
response = llm_gemini.generate(messages=msgs)

print(response.text)