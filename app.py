from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st

from providers.azure_openai import AzureOpenAIProvider
from providers.gemini import GeminiProvider
from providers.bedrock import AWSBedrockProvider

from use_cases.chat import ChatUseCase
from use_cases.summarize import SummarizeUseCase

st.set_page_config(page_title="AI Test Box", page_icon="🚀", layout="centered")
st.title("🚀 AI Test Box")

PROVIDERS = {
    "Azure OpenAI": AzureOpenAIProvider,
    "Google Gemini": GeminiProvider,
    "AWS Bedrock": AWSBedrockProvider,
}

USE_CASES = {
    "Chat": ChatUseCase,
    "Summarize": SummarizeUseCase,
}

if "last_provider" not in st.session_state:
    st.session_state["last_provider"] = None
if "last_use_case" not in st.session_state:
    st.session_state["last_use_case"] = None

with st.sidebar:
    st.header("Configuration")
    provider_name = st.selectbox("Provider", list(PROVIDERS.keys()), key="provider_select")
    use_case_name = st.selectbox("Use Case", list(USE_CASES.keys()), key="use_case_select")

    if (
        st.session_state["last_provider"] != provider_name
        or st.session_state["last_use_case"] != use_case_name
    ):
        st.session_state.pop("result", None)
        st.session_state.pop("raw", None)
        st.session_state.pop("user_input", None)
        st.session_state.pop("system_prompt", None)

    st.session_state["last_provider"] = provider_name
    st.session_state["last_use_case"] = use_case_name

    creds_ok = False
    missing_vars = []

    if provider_name == "Azure OpenAI":
        required = [
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_DEPLOYMENT",
            "AZURE_OPENAI_API_VERSION",
        ]
        creds_ok = all(os.getenv(v) for v in required)
        missing_vars = [v for v in required if not os.getenv(v)]

    elif provider_name == "Google Gemini":
        required = [
            "GEMINI_API_KEY",
            "GEMINI_MODEL",
            "GEMINI_THINKING_BUDGET",
        ]
        creds_ok = all(os.getenv(v) for v in required)
        missing_vars = [v for v in required if not os.getenv(v)]

    elif provider_name == "AWS Bedrock":
        required = [
            "AWS_BEDROCK_API_KEY",
            "AWS_BEDROCK_API_KEY_ID",
            "AWS_REGION",
            "AWS_BEDROCK_MODEL",
            "AWS_BEDROCK_MAX_TOKENS",
            "AWS_BEDROCK_TEMPERATURE",
        ]
        creds_ok = all(os.getenv(v) for v in required)
        missing_vars = [v for v in required if not os.getenv(v)]

    st.markdown(f"**Credentials detected:** {'✅' if creds_ok else '⚠️ not detected'}")
    if not creds_ok and missing_vars:
        st.caption(f"Missing: {', '.join(missing_vars)}")

ProviderClass = PROVIDERS[provider_name]
UseCaseClass = USE_CASES[use_case_name]

provider = ProviderClass()
use_case = UseCaseClass()

st.subheader(f"{use_case_name} with {provider_name}")

user_input = st.text_area(
    "Input",
    value=st.session_state.get("user_input", ""),
    placeholder="Write your prompt, text to summarize, etc.",
    height=180
)
st.session_state["user_input"] = user_input

system_prompt = st.text_area(
    "System Prompt (optional)",
    value=st.session_state.get("system_prompt", ""),
    placeholder="e.g., You are a helpful assistant that answers concisely.",
    height=100
)
st.session_state["system_prompt"] = system_prompt

c_run, c_clear, c_raw = st.columns([1, 1, 1.4])
with c_run:
    run_btn = st.button("Run", type="primary", use_container_width=True)
with c_clear:
    clear_btn = st.button("Clear", use_container_width=True)
with c_raw:
    show_raw = st.checkbox("Show raw JSON", key="show_raw")

if clear_btn:
    st.session_state.pop("result", None)
    st.session_state.pop("raw", None)
    st.session_state.pop("user_input", None)
    st.session_state.pop("system_prompt", None)

if run_btn:
    if not user_input.strip():
        st.warning("Please provide some input.")
    else:
        with st.spinner("Generating..."):
            try:
                sys = system_prompt.strip() or None
                out = use_case.run(provider, user_input, system=sys)
                st.session_state["result"] = out.get("text", "")
                st.session_state["raw"] = out.get("raw", None)
            except Exception as e:
                st.error(f"Error: {e}")

if "result" in st.session_state:
    st.markdown("### Result")
    st.write(st.session_state["result"])

    if show_raw and st.session_state.get("raw") is not None:
        st.markdown("### Raw JSON")
        st.json(st.session_state["raw"])
