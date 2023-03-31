import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

file_name = os.path.join(os.path.dirname(__file__), 'mydata.jsonl')

openai.File.create(
  file=open(file_name, "rb"),
  purpose='fine-tune'
)