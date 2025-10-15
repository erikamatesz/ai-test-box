# 🧠 AI Test Box

AI Test Box is a modular generative AI playground built with Python and Streamlit.
It provides a unified framework for testing and comparing multiple AI providers such as Azure OpenAI, Google Gemini, and AWS Bedrock through a consistent interface and a set of reusable use cases such as chat, summarization, and job analysis.

## 📁 Project Structure

```sh
.
├── README.md
├── app.py
├── .env.example
├── providers
│   ├── azure_openai.py
│   ├── base.py
│   ├── bedrock.py
│   └── gemini.py
├── requirements.txt
└── use_cases
    ├── base.py
    ├── chat.py
    ├── jobs.py
    └── summarize.py
```

Main components:

* `app.py` – Streamlit entry point that loads provider options and orchestrates use cases.
* `providers/` – Provider adapters implementing a shared interface for Azure OpenAI, Gemini, and Bedrock.
* `use_cases/` – Reusable logic modules for different tasks (chat, summarization, etc.).
* `requirements.txt` – Project dependencies.
* `.env.example` – Environment variables for credentials and configuration.

## ⚙️ Setup Instructions

### 1. Clone the repository

```sh
git clone https://github.com/<your-username>/ai-test-box.git
cd ai-test-box
```

### 2. Create and activate a virtual environment

```sh
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and rename it:

```sh
cp .env.example .env
```

Fill in your credentials and settings:

```sh
# Azure OpenAI
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_DEPLOYMENT=
AZURE_OPENAI_API_VERSION=

# Google Gemini
GEMINI_API_KEY=
GEMINI_MODEL=
GEMINI_THINKING_BUDGET=

# AWS Bedrock
AWS_BEDROCK_API_KEY=
AWS_BEDROCK_API_KEY_ID=
AWS_REGION=
AWS_BEDROCK_MODEL=
AWS_BEDROCK_MAX_TOKENS=
AWS_BEDROCK_TEMPERATURE=
```

### 🔑 Obtaining API Keys and Credentials

You must create or access accounts on each provider’s console to obtain the required credentials:

- Azure OpenAI:
  Visit https://portal.azure.com → Azure OpenAI Resource → Keys and Endpoint.
  Copy the API key, endpoint, and deployment name for the desired model (e.g., gpt-4o-mini, gpt-4-turbo).
  Check API versions at https://learn.microsoft.com/en-us/azure/ai-services/openai/reference.

- Google Gemini:
  Go to https://aistudio.google.com → Get API key.
  Set the model (e.g., gemini-1.5-flash, gemini-1.5-pro) and an optional thinking budget if supported.

- AWS Bedrock:
  Log into https://console.aws.amazon.com/bedrock/
  Go to IAM → Users → Security Credentials to create an access key and secret key.
  Configure your preferred region (e.g., us-east-1) and model (e.g., anthropic.claude-3-sonnet-20240229-v1:0).

Make sure your keys are kept private and never committed to version control.

## 🚀 Running the App

Launch the Streamlit interface:

streamlit run app.py

Then open the URL provided by Streamlit (usually http://localhost:8501).

You’ll be able to:
* Select between Azure OpenAI, Google Gemini, and AWS Bedrock.
* Choose a use case (chat, summarization, or job analysis).
* Compare outputs across models in a simple, unified interface.

## 📦 Dependencies

From requirements.txt:

streamlit>=1.36.0
openai>=1.35.0
boto3>=1.34.0
google-genai==1.38.0
python-dotenv>=1.0.1

## 🧪 Extending AI Test Box

To add a new model or provider:

1. Create a new class in  `providers/` extending BaseProvider.
2. Implement the `generate()` or equivalent interface method.
3. Add a corresponding entry to the Streamlit UI in app.py.

To add a new use case:

1. Create a new class in `use_cases/` extending BaseUseCase.
2. Implement the `run()` method with your logic.
3. Register it in the app.

This modular structure allows you to quickly experiment with new APIs, tasks, or evaluation strategies.

## 🤝 Contributing

Contributions are welcome!  
If you’d like to improve AI Test Box — by adding new providers, extending use cases, or enhancing the UI — please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or fix:
   `git checkout -b feature/my-new-feature`
3. Make your changes and commit them:
   `git commit -m "Add new feature"`
4. Push your branch:
   `git push origin feature/my-new-feature`
5. Open a Pull Request describing your contribution.

Please ensure your code is clean, documented, and tested before submitting.