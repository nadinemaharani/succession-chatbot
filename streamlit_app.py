import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from vertexai import init
from vertexai.generative_models import GenerativeModel
from vertexai.preview.generative_models import GenerativeModel


# Init Vertex AI
creds = service_account.Credentials.from_service_account_file(
    "succession-chatbot-personal-1548effd5fe5.json"
)

init(
    project="succession-chatbot-personal",
    location="us-central1",
    credentials=creds
)

# Load model
model = GenerativeModel("gemini-2.0-flash")

# Load KB
kb = pd.read_excel("KB-Succession.xlsx")

st.title("💬 Succession Planning Chatbot")

def answer_with_gemini(prompt):
    prompt_lower = prompt.lower()

    # detect role from prompt
    roles = [r for r in kb["Target_Role"].unique() if str(r).lower() in prompt_lower]

    if not roles:
        return "❗ I couldn't identify any role from your question."

    role = roles[0].lower()
    matches = kb[kb["Target_Role"].str.lower() == role]

    if matches.empty:
        return "❗ No candidates found for that role."

    kb_context = "\n".join([
        f"{row['Name']} - {row['Current_Role']} → {row['Target_Role']}, "
        f"Exp {row['Experience']} yrs, Leadership {row['Leadership']}, "
        f"Success {row['Project_Success_Rate']}%, Review {row['Last_Review_Score']}"
        for _, row in matches.iterrows()
    ])

    response = model.generate_content(
        f"Candidate data:\n{kb_context}\n\nUser question: {prompt}"
    )

    return response.text

prompt = st.chat_input("Ask about successors...")

if prompt:
    st.chat_message("user").markdown(prompt)
    ans = answer_with_gemini(prompt)
    st.chat_message("assistant").markdown(ans)
