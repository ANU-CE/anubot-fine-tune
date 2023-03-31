import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

content = openai.File.download("file-xcG5s4EJ0j0UiqtGzgWrW440")
print(content)