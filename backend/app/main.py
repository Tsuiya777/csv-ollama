from fastapi import FastAPI, UploadFile, File
import pandas as pd
import requests

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    """
    CSVを読み込み、行数・列数と先頭5行を返す
    """
    df = pd.read_csv(file.file)
    prompt = "The God"
    print(prompt)
    print(ollama(prompt))
    return {"columns": df.columns.tolist(), "data": df.to_dict(orient="records")}



def ollama(text_to_analyze):
    url = "http://ollama:11434/api/generate"
    
    payload = {
        "model": "gemma3:4b",
        "system": "You will read the given text and respond with a number from 1 to 9 that you think best describes the content. 1 is about people, 2 is about things, and 3 is everything else.",
        "prompt": f"{text_to_analyze}",
        "stream": False   # ストリームを無効化
    }

    response = requests.post(url, json=payload, stream=True)
    # return response.iter_lines().decode("utf-8")


    for line in response.iter_lines():
        if line:
            data = line.decode("utf-8")
            break

    return data
