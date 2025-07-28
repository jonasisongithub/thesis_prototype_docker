import json
import os
import sys
from huggingface_hub import hf_hub_download # type: ignore
from huggingface_hub import InferenceClient # type: ignore
import streamlit as st # type: ignore
from google import genai
from google.genai import types # type: ignore
from datetime import datetime


# CONFIG laden
config_path = "./config"
sys.path.append(config_path)
import config_interview  #type: ignore
print("Config geladen")


CHOSEN_MODEL = st.secrets["CHOSEN_MODEL"]
client = genai.Client(api_key=st.secrets['gemini_access_token'])

def step1_icebreakerquestion():
    name = st.session_state.get("name")
    position = st.session_state.get("position")
    task = st.session_state.get("task")
    context = st.session_state.get("context")
    guideline = st.session_state.get("guideline")

    interviewer_prompt = config_interview.ROLE_INTERVIEWER.format(
        name=name,
        position=position,
        task=task,
        context=context,
        guideline=guideline
    )
    
    prompt_icebreaker = f"""
    {interviewer_prompt}

    You are about to start a qualitative expert interview with {name}. Your first task is to greet {name} warmly, thank them for their time, and initiate the conversation with an engaging opening question.

    **Your Goal for the Opening:**
    * Help the interviewee feel at ease and comfortable.
    * Establish a personal connection and a positive, human-like tone.
    * Invite them to share insights about their role and what they personally enjoy about their work at die GEMA.
    * Begin the interview naturally and unscripted.

    **Output Requirements:**
    * Generate *only* the opening message and one warm, personal opening question.
    * The message must be phrased as if spoken directly by a friendly, professional human interviewer.
    * Use clear, conversational German and the informal "Du" form.
    * Avoid robotic or generic phrasing.
    * Do not include any quotation marks in your message.

    Begin now.
    """
    

    response = client.models.generate_content(
    model=CHOSEN_MODEL,
    contents=prompt_icebreaker,
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=300)),
    )
   
    question = response.text
    print("Returned icebreaker question")
    return question


def step2_questions(last_user_response, full_chat_history):
    name = st.session_state.get("name")
    position = st.session_state.get("position")
    task = st.session_state.get("task")
    context = st.session_state.get("context")
    guideline = st.session_state.get("guideline")

    interviewer_prompt = config_interview.ROLE_INTERVIEWER.format(
        name=name,
        position=position,
        task=task,
        context=context,
        guideline=guideline
    )

    prompt_question = f"""{interviewer_prompt}

    You are continuing a qualitative expert interview with an employee of die GEMA. Your task is to generate the most appropriate next interview question or statement, based on the ongoing conversation and your overarching goal of uncovering undocumented expert knowledge.

    **Decision Logic for Next Action:**
    * **Elaboration Needed:** If the last user response was brief, vague, or highlighted a new, interesting, or emotionally relevant point, formulate a thoughtful follow-up question to encourage deeper insights. Use clarification and paraphrasing to ensure understanding.
    * **Topic Covered:** If the last user response feels comprehensive and the current sub-topic from the interview guideline seems sufficiently explored, transition smoothly to the next relevant question from the guideline. You may rephrase or reorder questions from the guideline for optimal flow.
    * **Contextual Awareness:** Continuously refer to the full chat history and the existing documented knowledge. Do *not* ask questions that have already been answered, discussed, or where the interviewee explicitly stated there is no further information to share. Focus on knowledge gaps.
    * **Adaptation:** Be agile with synonyms based on the context of the conversation to maintain a natural dialogue.

    **Output Requirements:**
    * Respond *only* with the next appropriate interview question or a statement that encourages further sharing or transitions the topic.
    * The output must be in **German** and use the **informal "Du" form**.
    * Your response must sound like it's from a human-led, warm, and intuitive conversation. Do not mention that you are following a guideline or that you are an AI.
    * Formulate questions sensitively to avoid critical interpretations by the interviewee.

    **Special Instructions for Interview Conclusion:**
    * If, based on the interview guideline, full chat history, and last user response, it's appropriate to conclude the interview (e.g., all topics covered, interviewee indicates readiness to end), you may ask a polite closing question such as "Gibt es noch etwas, das du teilen möchtest?" or "Hast du noch letzte Gedanken oder Fragen?".
    * If the interviewee explicitly confirms they wish to end the interview after a closing question, your *only* output must be the specific code: "**t435kd90**". Do not send any other text in this specific case. If he does not explicitly confirm, continue with the next question.

    ---
    **Interviewee’s Last Response to Consider:**
    {last_user_response}

    ---
    **Full Chat History for Context:**
    {full_chat_history}
    """
    
    response = client.models.generate_content(
    model=CHOSEN_MODEL,
    contents=prompt_question,
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=300)),
    )
   
    question = response.text
    print("Returned normal question")
    return question



def end_conversation(full_chat_history):
    name = st.session_state.get("name")
    position = st.session_state.get("position")
    task = st.session_state.get("task")
    context = st.session_state.get("context")
    guideline = st.session_state.get("guideline")

    interviewer_prompt = config_interview.ROLE_INTERVIEWER.format(
        name=name,
        position=position,
        task=task,
        context=context,
        guideline=guideline
    )

    prompt_ending = f"""{interviewer_prompt}

    You are now at the end of the expert interview. You have access to the full chat history, which reflects the entire conversation.

    ---
    **Full Chat History for Context:**
    {full_chat_history}
    ---

    Please thank the interviewee warmly for their openness, the time they took, and the knowledge they shared. **Crucially, adapt the *intensity* of your gratitude and the acknowledgement of "valuable knowledge" to the actual extent and perceived quality of the information shared throughout the `full_chat_history`.** The thank you should always be present and appreciative, but the level of enthusiasm or emphasis on "valuable knowledge" should align with the reality of the conversation.

    Inform them that:
    – Their knowledge contribution will be compiled and sent to them via email afterward.
    – It would be great if they could pass the compiled article or summary to our internal knowledge management team, so that it can be included in the official documentation.

    Your output must be:
    – In **German**
    – Using the **informal "Du" form**
    – Warm, clear, appreciative, and natural – as if you are a thoughtful human wrapping up a good conversation.
    – Do not reference that you are an AI or mention the interview process technically.

    Begin now."""

    
    response = client.models.generate_content(
    model=CHOSEN_MODEL,
    contents=prompt_ending,
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=300)),
    )
   
    question = response.text
    print("Returned last answer")
    return question


def transcript_summary(filepath):
    """
    Liest ein Transkript, generiert eine Zusammenfassung neuen Wissens 
    und speichert diese als Markdown-Datei.
    """
    transcript_content = ""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            transcript_content = file.read()
    except FileNotFoundError:
        print(f"Datei nicht gefunden: {filepath}")
        return
    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {e}")
        return
    
    context = st.session_state.get("context")

    prompt_summary = f"""You are given the transcript of an expert interview. The transcript consists of alternating lines from "ASSISTANT" (the interviewer asking questions) and "USER" (the interviewee responding). The responses from the USER represent the knowledge shared during the conversation.

        Your task is to write a **German knowledge article** for the internal knowledge management system at GEMA.

        **Important constraints:**
        – You are also given context, which contains all previously documented knowledge on this topic
        – Your output must include **only new knowledge** that was not already present in the context
        – Do not include duplicate or redundant information
        – If no relevant new knowledge is found in the transcript, return a very short note explaining that no substantial additions were identified

        **Content guidelines:**
        – The article must not mention the interview, the interviewer, or the interviewee
        – Focus entirely on the knowledge gained, not the process by which it was collected
        – Use clear, precise, and professional language in **German**
        – You may use headings, subheadings, bullet points, or lists — but only when helpful for clarity and structure
        – If the new knowledge is narrow, specific, or limited in scope, that is perfectly acceptable — do not invent or expand beyond what was said

        **Output:**
        – A concise, well-structured German knowledge article that presents only the **new insights** or **previously undocumented details**
        – Do not include any reference to the transcript format or speakers
        - Use markdown formatting in your response, e.g. headings, bullet points, etc.

        Here is the input:
        – Transcript: {transcript_content}
        – Existing context knowledge: {context}"""

    try:
        response = client.models.generate_content(
            model=CHOSEN_MODEL,
            contents= prompt_summary,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=-1)),
        )
        summary = response.text
        
        output_dir = "./output/summaries/"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        
        output_filename = f"summary_{timestamp}_{base_name}.md"
        output_filepath = os.path.join(output_dir, output_filename)

        try:
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(summary)
            print(f"Zusammenfassung erfolgreich generiert und gespeichert: {output_filepath}")
        except Exception as e:
            print(f"Fehler beim Speichern der Datei: {e}")
        
    except Exception as e:
        print(f"Fehler bei der KI-Anfrage: {e}")