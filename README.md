
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
2. Create new Docker Artifact in GCP Artifact registry and copy path
3. Cloud console: docker build -t path/CHOOSE_NAME:v01 .
4. Cloud console: docker push path/CHOOSE_NAME:v01
5. Go to Google Cloud Rund and start a new service by selscting correct image from artifact registry
6. Attach a GCP Bucket as volume and mount it with mount-path /interview_output --> You'll find all summaries and transcripts in this bucket


## Getting Started

```bash
git clone git@github.com:jonasisongithub/Thesis_Prototype.git



