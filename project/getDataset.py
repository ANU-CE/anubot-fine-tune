import pandas as pd
import os
from openai.embeddings_utils import get_embedding
import tiktoken

# embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191

# path to file
fileName = "output.csv"
filePath = os.path.join(os.path.dirname(__file__), fileName)

# read csv file
df = pd.read_csv(filePath, encoding="cp949")
encoding = tiktoken.get_encoding(embedding_encoding)

print("starting to embed")

df["embedding"] = df.textData.apply(lambda x: get_embedding(x, engine=embedding_model))
df.to_csv("phoneBook_with_embeddings.csv")

print("finished embedding")