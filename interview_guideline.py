def generate_interview_guideline(position, topic, context):
    import os
    import sys
    from huggingface_hub import hf_hub_download # type: ignore
    from huggingface_hub import InferenceClient # type: ignore
    import streamlit as st # type: ignore
    from google import genai
    from google.genai import types  # type: ignore
  
  
    CHOSEN_MODEL = st.secrets["CHOSEN_MODEL"]
    client = genai.Client(api_key=st.secrets['gemini_access_token'])
    
    # CONFIG laden
    config_path = "./config"
    sys.path.append(config_path)
    import config_leitfaden #type: ignore
    print("Config geladen")



    # STEP 1: SAMMELN
    response = client.models.generate_content(
    model=CHOSEN_MODEL,
    contents=f"""{config_leitfaden.ROLE}

    You are preparing for a qualitative expert interview in the context of **die GEMA** organization with a colleague whose position is **{position}**. The overarching goal is to uncover as much **relevant and potentially undocumented knowledge** as possible related to the topic: "{topic}".

    Your task is to generate questions that encourage the expert to share deep insights, experiences, and perspectives. Therefore, it's crucial to ask relevant, non-trivial, and open-ended questions that truly elicit their unique, tacit knowledge.

    **Important Contextual Information for Question Generation:**
    * **Existing Documented Knowledge:** You are provided with existing knowledge related to the topic. **Crucially, ensure your questions go beyond this existing documentation and primarily aim to uncover new, undocumented insights.** Do not ask about information that is already written down.
        * Existing knowledge: {context}

    **Instructions for Question Generation:**
    * Brainstorm and generate **30 diverse, open-ended interview questions**.
    * These questions must cover a wide range of possible subtopics, angles, and dimensions of the subject, including: technical, organizational, procedural, individual, and strategic aspects.
    * Consider eliciting tacit knowledge, personal experience, challenges, best practices, edge cases, and forward-looking perspectives.
    * All questions must be phrased in **German**, using the **informal "Du" form**.
    * The questions should be inherently open, respectful, neutral, and designed to elicit thoughtful, knowledge-rich answers.
    * **Do not include any section headers, explanations, or commentary in your output.**
    * Return **only the numbered list of interview questions.**

    Begin now.""",

    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=300)),
    )
    step1_sammeln = response.text
    print("Step 1 ausgeführt")

    # STEP 2: PRÜFEN
    response = client.models.generate_content(
    model=CHOSEN_MODEL,
    contents=f"""{config_leitfaden.ROLE} 

    You are continuing the development of a qualitative interview guide based on the **SPSS method by Helfferich (2009)**, specifically applying **Step 2: PRÜFEN (Review)**.

    **Original List of Brainstormed Questions from Step 1:**
    {step1_sammeln}

    **Instructions for Review and Filtering:**
    * Evaluate each question from the provided list based on the following criteria:
        * **Relevance:** Does the question clearly relate to the specific topic "{topic}"?
        * **Potential for New Knowledge:** Does it have strong potential to uncover relevant, *new*, or undocumented expert knowledge, moving beyond what is already known or documented in the {context}?
        * **Question Quality:** Is the question truly open-ended, neutral, clearly formulated, and suitable for a respectful expert interview (in **Du-form**, German)?
    * **Filtering Rule:** Remove all questions that are:
        * Redundant or repetitive within the list.
        * Irrelevant to the core topic or the goal of uncovering new knowledge.
        * Leading or suggestive.
        * Vague, ambiguous, or unclear.
        * Likely to elicit already-documented information (i.e., not uncover new insights).
    * **Mandatory Filtering:** You **must remove at least 20% of the original questions**, prioritizing the least relevant ones. **Never keep all questions** from the previous step; always filter them down to a more relevant and focused set.
    * **Do not generate any new questions.** Work strictly with the provided list.

    **Output Requirements:**
    * Return **only the revised, filtered, and optimized list of questions** as a **numbered list**.
    * All questions must remain phrased in **German**.
    * **Do not include any headings, commentary, explanations of your changes, or lists of removed items.** Only the final, filtered list.

    Begin now.
    """,

    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=300)),
    )
    step2_pruefen= response.text
    print("Step 2 ausgeführt")

    # STEP 3: SORTIEREN
    response = client.models.generate_content(
    model=CHOSEN_MODEL,
    contents=f"""{config_leitfaden.ROLE} 

    You are continuing the development of a qualitative interview guide based on the **SPSS method by Helfferich (2009)**, specifically applying **Step 3: SORTIEREN (Sorting)**.

    **Filtered List of Questions from Step 2:**
    {step2_pruefen}

    **Instructions for Sorting and Structuring:**
    * Analyze all questions from the provided list and group them into **thematically coherent sections (question clusters / thematic blocks)**.
    * **Number of Sections:** You **must create a minimum of 3 and a maximum of 5 distinct thematic sections.**
    * **Questions per Section:** Each thematic section **must contain at least 3 questions.**
    * **Meaningful Headings:** Create short, descriptive, and meaningful **German headings** for each thematic block (e.g., "Hintergrund & Kontext", "Aktuelle Arbeitsweisen", "Herausforderungen", "Zukunftsperspektiven").
    * **Logical Flow:** Ensure a **logical and natural conversational flow** across the entire guide:
        * Start with easier, introductory, or general context questions.
        * Move progressively to deeper, more specific, or potentially sensitive topics in the middle.
        * Conclude with reflective, summarizing, or forward-looking questions.
    * Place each question into its most appropriate block and order them logically within that block.
    * **Do not generate any new questions.** Work strictly with the provided list.

    **Output Format:**
    * Return **only the sorted interview questions structured by thematic blocks**.
    * Each block should have its **short, descriptive German heading** followed by a **numbered list of the relevant questions**.
    * All questions must be shown in **German**, in the **informal "Du" form**.
    * **Do not include any explanations or commentary – only the structured output.**

    Begin now.
    """,

    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=300)),
    )
    step3_sortieren= response.text
    print("Step 3 ausgeführt")



    # STEP 4: SUBSUMIEREN
    response = client.models.generate_content(
    model=CHOSEN_MODEL,
    contents=f"""{config_leitfaden.ROLE} 
    You are completing **Step 4: SUBSUMIEREN (Subsuming)** of the **SPSS method by Helfferich (2009)**.

    **Structured List of Interview Questions from Step 3:**
    {step3_sortieren}

    **Instructions for Condensing and Synthesizing:**
    * For each thematic block, identify overlapping, redundant, or closely related questions.
    * **Condense and synthesize these questions into 1 to 2 comprehensive main questions (Leitfragen) per block.**
    * Each main question must **represent the core intent** of its block and effectively *subsume* the underlying detailed questions into a broader inquiry.
    * **Crucially, do not simply list or rephrase existing questions.** Actively **merge and reformulate them into thematic umbrella questions** that cover the essence of the original set.
    * Ensure the reformulated Leitfragen remain **open-ended, neutral, exploratory, and suitable for an expert interview (in Du-form, German)**.

    **Output Format:**
    * The output must be in **JSON format**.
    * The JSON object should contain a key (e.g., `"sections"` or `"leitfaden"`) whose value is an array of section objects.
    * Each section object must contain:
        * A key for the **German heading** (e.g., `"heading": "Herausforderungen"`).
        * A key for the **Leitfragen** (e.g., `"questions"`), whose value is an array containing 1 to 2 numbered Leitfragen in German.
    * **Very Important:** Do **not** include any explanations, commentary, or headings outside of the specified JSON structure. Only the final, structured JSON output.
    Begin now.""",

    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=300)),
    )
    step4_subsumieren= response.text
    print("Step 4 ausgeführt")


    return step4_subsumieren



