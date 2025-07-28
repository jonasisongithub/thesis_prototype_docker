import requests # type: ignore
import re
import streamlit as st # type: ignore
# FUNCTION for plain text retrieval
def context_from_plain_docs(topic: str) -> str:
    topic= "Return all information you can find about: " + topic
    prompt = topic.replace(" ", "20der%25")
    url = f"https://app.customgpt.ai/api/v1/projects/plugins/{st.secrets['customgpt_project_id']}/get_context?prompt={prompt}"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"API-Error:  {response.status_code}")

    data = response.json()
    context_raw = data.get("context", "")

    # only take titel sections
    titles = re.findall(r"title:\s*(.+)", context_raw)

    # remove duplicates
    seen = set()
    unique_titles = []
    for t in titles:
        clean = t.strip()
        if clean not in seen:
            seen.add(clean)
            unique_titles.append(clean)

    return "\n\n".join(unique_titles)


# FUNCTION for full text chatbot response
def context_from_chatbot(topic: str) -> str:
    url = "https://app.customgpt.ai/api/v1/projects/73419/conversations/15460113434/messages?stream=false&lang=de"
    payload = {
        "response_source": "own_content",
        "prompt": "Return all information you can find about: " + topic,
        "chatbot_model": "gpt-4-o"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": st.secrets["customgpt_bearer"]
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"API-Error: {response.status_code}")

    data = response.json()

    try:
        content = data["data"]["openai_response"]
    except KeyError:
        raise Exception("openai_response couldnt be found")

    titles = re.findall(r"title:\s*(.+)", content)
    if not titles:
        return content.strip()

    #duplicate removal
    seen = set()
    unique_titles = []
    for title in titles:
        clean = title.strip()
        if clean not in seen:
            seen.add(clean)
            unique_titles.append(clean)

    return "\n\n".join(unique_titles)


# METHOD to call to get all the context for a given topic
def get_context(topic):
    chatbot_answer = context_from_chatbot(topic)
    plain_answer = context_from_plain_docs(topic)

    context = chatbot_answer + "\n\n" + plain_answer
    print(context)
    return context
