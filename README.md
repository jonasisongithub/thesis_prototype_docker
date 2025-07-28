
# LLM-Powered Expert Interview Assistant (Prototype)

## Overview

This repository contains the prototype implementation for a Master's thesis project focused on **AI-supported expert interviews using Large Language Models (LLMs)**. The core objective is to explore how LLMs can conduct **natural, empathic, and knowledge-generating interviews** with domain experts in organizational settings.

The prototype enables a conversational agent—guided by a predefined interview structure (guideline) and contextual background knowledge—to dynamically interact with human interviewees, **ask follow-up questions**, and **elicit undocumented expert knowledge**, while maintaining a **natural conversation flow**.

---

## Project Goals

- **Human-like interaction**: Interviews should feel personal, intuitive, and non-robotic—using informal German ("Du"-Form) and a warm tone.
- **Semi-structured guidance**: The system follows a provided interview guideline but makes real-time decisions on skipping, reordering, or deepening questions.
- **Knowledge elicitation**: The assistant aims to uncover expert knowledge that is not yet documented—based on comparison with a provided knowledge base.
- **Balance of structure and openness**: The interviewer adapts dynamically, deciding when to stay in a topic or return to the structure.

---

## Features

- **Role-based prompt architecture** using Helfferich’s SPSS method for qualitative interview guide design  
- **System and persona prompts** tailored for expert knowledge interviews at GEMA (German copyright organization)  
- **LLM-driven interview logic**, including dynamic guideline handling, follow-up reasoning, and natural transitions  
- Integration of contextual knowledge to avoid redundant questions  
- Full conversation in **German**, informal **Du-Form**, warm and appreciative

---

## Technologies Used

- Python Frontend based on Streamlit
- OpenAI / GPT APIs (or other LLM backends)
- RAG context provided by CustomGPT.ai
- Modular prompt chaining and session state tracking

---

## Contact / Contributions

Feel free to reach out for academic collaboration, feedback, or discussion.

Author: Jonas Walther

Institution: Universität Leipzig

Thesis title: "Large Language Models zur Wissensgewinnung: Durchführung von KI-gestützten Experteninterviews"

---

## How to deploy on GCP

1. Login to GCP console and open the cloud shell
2. Create fine-grained personal access token for your Github Account
3. git clone https://github.com/jonasisongithub/Thesis_Prototype.git
4. Authenticate with username and Access Token
5. Create an virtual environment within the correct path "python3 -m venv nameofthevenv and activate it with source name/bin/activate
6. Install all the required libraries with pip install -r requirements.txt from the repository
7. Export needed information:   export GCP_PROJECT='aviapi' 
                                export GCP_REGION='us-central1' 
                                export AR_REPO='gemini_mtgcalc-repo' 
                                export SERVICE_NAME='gemini-mtgcalc-streamlit-app' 
                                gcloud artifacts repositories create "$AR_REPO" --location="$GCP_REGION" --repositoryformat=Docker gcloud auth configure-docker "$GCP_REGION-docker.pkg.dev" 
                                gcloud builds submit --tag "$GCP_REGIONdocker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME" 
                                gcloud run deploy "$SERVICE_NAME"
                                \ 
                                --port=8080 \ 
                                --image="$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME" \ 
                                --allow-unauthenticated \ 
                                --region=$GCP_REGION \ 
                                --platform=managed \ 
                                --project=$GCP_PROJECT \ 
                                --set-env-vars=GCP_PROJECT=$GCP_PROJECT,GCP_REGION=$GCP_REGION


## Getting Started

```bash
git clone git@github.com:jonasisongithub/Thesis_Prototype.git



