import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

openai.File.delete("file-xcG5s4EJ0j0UiqtGzgWrW440")