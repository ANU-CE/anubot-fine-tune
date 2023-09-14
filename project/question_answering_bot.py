import ast  # for converting embeddings saved as strings back to arrays
import openai  # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
from scipy import spatial  # for calculating vector similarities for search
import os  # for accessing environment variables

# api key
openai.api_key = os.getenv("OPENAI_API_KEY")

# models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"

# settings for the embedding model
filename = "phoneBook_with_embeddings.csv"
embeddings_path = filename = os.path.join(os.path.dirname(__file__), filename)

# prompt settings
introduction_prompt = 'Use the below data to answer the subsequent question. If the answer cannot be found in the phone book, write "I could not find an answer."'
question = "054-820-0000 어디 전화번호야"
accuracy = 10 # this is the number of results to return for the search


df = pd.read_csv(embeddings_path, encoding="utf-8")

# convert embeddings from CSV str type back to list type
df['embedding'] = df['embedding'].apply(ast.literal_eval) # ast.literal_eval() converts a string to a list


# search function
def strings_ranked_by_relatedness(
    query: str, # query is the string you want to search for
    df: pd.DataFrame, # df is the dataframe containing the strings and embeddings
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y), ## this is the function used to calculate relatedness
    top_n: int = accuracy # this is the number of results to return
) -> tuple[list[str], list[float]]: # this is the type annotation for the return value
    
    #####################################################################################
    ###Returns a list of strings and relatednesses, sorted from most related to least.###
    #####################################################################################

    query_embedding_response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=query,
    )

    query_embedding = query_embedding_response["data"][0]["embedding"] # get the embedding from the response
    
    strings_and_relatednesses = [
        (row["textData"], relatedness_fn(query_embedding, row["embedding"])) # calculate relatedness
        for i, row in df.iterrows() # iterate through the dataframe
    ]

    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True) # sort by relatedness
    strings, relatednesses = zip(*strings_and_relatednesses) # unzip into two lists
    return strings[:top_n], relatednesses[:top_n] # return the top n results


# Return the number of tokens in a string.
def num_tokens(text: str, model: str = GPT_MODEL) -> int: 
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


# Return a message for GPT, with relevant source texts pulled from a dataframe.
def query_message(
    query: str,
    df: pd.DataFrame,
    model: str,
    token_budget: int
) -> str:
    

    strings, relatednesses = strings_ranked_by_relatedness(query, df) # get the top results
    introduction = introduction_prompt
    question = f"\n\nQuestion: {query}" 
    message = introduction
    for string in strings: # iterate through the top results
        next_article = f'\n\nsection:\n"""\n{string}\n"""' # add the next article to the message
        
        if (num_tokens(message + next_article + question, model=model) > token_budget): # if the message is too long, stop
            break
        else: # otherwise, keep going
            message += next_article
    
    return message + question


# Ask a question using GPT, with relevant source texts pulled from a dataframe.
def ask(
    query: str,
    df: pd.DataFrame = df,
    model: str = GPT_MODEL,
    token_budget: int = 4096 - 500,
    print_message: bool = False,
) -> str:
    message = query_message(query, df, model=model, token_budget=token_budget)
    if print_message:
        print(message)
    
    messages = [
        {"role": "system", "content": "You should answer questions"},
        {"role": "user", "content": message},
    ]
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0
    )
    
    response_message = response["choices"][0]["message"]["content"]
    return response_message


print(ask(question, print_message=True))