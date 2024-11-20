import requests
import json

def score(prompt):
    "Output: answer_llm"
    
    url = 'http://4.144.34.206:8089/rag_completion'
    headers  =  {"Content-Type": "application/json"}

    payload = json.dumps({"prompt": f"{prompt}"})

    response = requests.request("POST", url, headers=headers, data=payload)

    answer_llm = response.json()['response']
    sources = response.json()['source_0'] + response.json()['source_1']


    return answer_llm, sources
