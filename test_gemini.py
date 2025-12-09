from vertexai import init
from vertexai.generative_models import GenerativeModel

# Use env var GOOGLE_APPLICATION_CREDENTIALS
init(project="succession-chatbot-personal", location="us-central1")

model = GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Halo Gemini, tes pertama!")
print(response.text)

