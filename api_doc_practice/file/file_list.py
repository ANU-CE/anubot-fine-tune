import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.File.list())
