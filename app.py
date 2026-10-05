import os

import requests
import streamlit as st

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
OLLAMA_URL = f"{OLLAMA_HOST}/api/chat"
MODEL = os.getenv("STUDYBUDDY_MODEL", "qwen2.5:1.5b")

SYSTEM_PROMPT = """You are StudyBuddy, a friendly local AI viva/practice partner.
Help a college student prepare for exams and technical interviews.
Be concise, practical, and encouraging.
When asked a technical question:
1. Give a simple explanation.
2. Give a small example when useful.
3. Ask one follow-up question or mini quiz question.
Never claim to know private information that was not provided.
"""

st.set_page_config(page_title="StudyBuddy", page_icon="🎓", layout="centered")
st.title("🎓 StudyBuddy")
st.caption("A private, local AI practice partner for your next viva or interview.")

with st.sidebar:
    st.header("Practice mode")
    mode = st.selectbox("Choose a mode", ["Viva Practice", "Interview Practice", "Explain a Topic"])
    st.info(f"Prompts are sent to Ollama at {OLLAMA_HOST}. The default is local: localhost.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask something like: Explain HashMap in simple words")

if prompt and prompt.strip():
    prompt = prompt.strip()
    with st.chat_message("user"):
        st.markdown(prompt)

    mode_instruction = {
        "Viva Practice": "Act like a viva examiner. Ask one question at a time and evaluate the student's answer.",
        "Interview Practice": "Act like a software engineering interviewer. Focus on Java, OOP, DSA, DBMS and networking.",
        "Explain a Topic": "Teach the topic from beginner level using simple language and examples."
    }[mode]

    # Keep only recent conversation context and commit the turn after a successful
    # response. Failed requests must not leave unanswered user turns in history.
    conversation = st.session_state.messages[-8:] + [{"role": "user", "content": prompt}]
    messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n" + mode_instruction}]
    messages += conversation

    with st.chat_message("assistant"):
        try:
            response = requests.post(
                OLLAMA_URL,
                json={"model": MODEL, "messages": messages, "stream": False},
                timeout=120,
            )
            response.raise_for_status()
            payload = response.json()
            if payload.get("error"):
                raise ValueError(payload["error"])
            answer = payload.get("message", {}).get("content", "").strip()
            if not answer:
                raise ValueError("Ollama returned an empty response.")
            st.markdown(answer)
            st.session_state.messages.extend(
                [
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": answer},
                ]
            )
        except requests.exceptions.ConnectionError:
            st.error(
                f"Could not reach Ollama at {OLLAMA_HOST}. Start Ollama, then run "
                f"`ollama pull {MODEL}` in PowerShell or Command Prompt."
            )
        except requests.exceptions.Timeout:
            st.error("Ollama took too long to respond. Try again or use a smaller model.")
        except requests.exceptions.HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 404:
                st.error(f"Model `{MODEL}` is not available. Run `ollama pull {MODEL}`.")
            else:
                st.error(f"Ollama returned an HTTP error: {exc}")
        except (ValueError, requests.exceptions.RequestException) as exc:
            st.error(f"Could not get a valid response from Ollama: {exc}")
        except Exception as exc:
            st.error(f"Something went wrong: {exc}")