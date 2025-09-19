from fastapi import FastAPI, UploadFile, File
import pandas as pd
import requests
import json

import os

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    """
    CSVを読み込み、行数・列数と先頭5行を返す
    """
    df = pd.read_csv(file.file)
    print("--- before ---")
    print(df.head())

    for index, row in df.iterrows():
        # print(f"index={index}, sentence={row['sentence']}, classifed={row['classifed']}")
        prompt = row['sentence']

        json_str = ollama(prompt)
        json_data = json.loads(json_str)
        df.loc[index, 'classifed'] = json_data['response']
        # row['classifed'] = json_data['response']
        # print(row['classifed'])
    
    """
    prompt = "The God"
    print(prompt)
    print(ollama(prompt))
    """
    print("--- after ---")
    print(df.head())
    return {"columns": df.columns.tolist(), "data": df.to_dict(orient="records")}

def ollama(text_to_analyze):

    # Connection Info to Ollama
    url = "http://ollama:11434/api/generate"
    payload = {
        "model": "gemma3:4b",
        "system": "You will read the given text and respond with a number from 1 to 9 that you think best describes the content. 1 is about people, 2 is about things, and 3 is everything else.",
        "prompt": f"{text_to_analyze}",
        "stream": False   # ストリームを無効化
    }

    # Process data
    response = requests.post(url, json=payload, stream=True)

    for line in response.iter_lines():
        if line:
            data = line.decode("utf-8")
            break

    return data

if __name__ == "__main__":
    current_directory = os.getcwd()
    print(current_directory)

    filename = "./testdata/Book2.csv"
    df = pd.read_csv(filename)
    print(df.head())
    # print(df["sentence", "classifed"])
    # print(df["sentence"])
    print(df.loc[0, "sentence"])
    print(df.loc[0, "classifed"])


    df.loc[0, "classifed"] = "a"
    print(df.loc[0, "classifed"])