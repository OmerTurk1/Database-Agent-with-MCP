from openai import OpenAI

client = OpenAI()
MODEL = "gpt-4o-mini"

def send_to_model(messages, tools=None):
    params = {
        "model": MODEL,
        "messages": messages
    }
    if tools:
        params["tools"] = tools
        
    return client.chat.completions.create(**params)