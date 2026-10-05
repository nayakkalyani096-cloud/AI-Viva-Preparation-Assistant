# StudyBuddy

StudyBuddy is a local AI practice partner built for a college friend preparing for technical vivas and interviews. It offers viva practice, interview practice, and topic explanations through a small Streamlit chat interface.

## How it works

The Python app sends the current prompt and recent chat history to the Ollama API running on your computer. Ollama runs the `qwen2.5:1.5b` model locally. StudyBuddy does not need an API key or a hosted AI service. The first model download needs an internet connection; later inference uses the local Ollama service.

## Requirements

- Windows 10/11, macOS, or Linux
- Python 3.10 or newer
- [Ollama](https://ollama.com/download) installed and running
- About 1 GB of disk space for the default Qwen2.5 1.5B model ([986 MB in Ollama's library](https://ollama.com/library/qwen2.5%3A1.5b)); running it also needs memory for the model and app

## Windows setup (PowerShell)

Open PowerShell in the project folder (the folder containing `app.py`), then run:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull qwen2.5:1.5b
ollama run qwen2.5:1.5b
```

The last command opens a model prompt. Type a short question to verify the model, then enter `/bye` to return to PowerShell. Ollama for Windows normally runs in the background after installation. If the command says it cannot connect, start the Ollama app from the Start menu. You can also run `ollama serve` in a separate terminal if the service is not already running.

Start StudyBuddy from the same project folder:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local address printed by Streamlit (usually `http://localhost:8501`). Keep Ollama running while you use the app.

## macOS / Linux setup

From the project folder (the folder containing `app.py`):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
ollama pull qwen2.5:1.5b
ollama run qwen2.5:1.5b
```

After verifying the model with a short prompt and `/bye`, start the app:

```bash
streamlit run app.py
```

Open the local address printed by Streamlit and leave Ollama running in the background.

## Configuration

By default, StudyBuddy connects to `http://localhost:11434` and uses `qwen2.5:1.5b`. Set these optional environment variables before starting Streamlit to use a different local Ollama address or an already-pulled Ollama model:

- `OLLAMA_HOST` — Ollama base URL, for example `http://localhost:11434`
- `STUDYBUDDY_MODEL` — Ollama model tag, for example `qwen2.5:1.5b`

Keep `OLLAMA_HOST` on your own machine for local use. Ollama's API does not provide authentication by default; do not expose a remote Ollama server to an untrusted network.

PowerShell example:

```powershell
$env:STUDYBUDDY_MODEL = "qwen2.5:1.5b"
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Troubleshooting

- **Could not reach Ollama:** open the Ollama app or run `ollama serve` in a separate terminal. The app expects the Ollama API at the configured host.
- **Model not available / HTTP 404:** run `ollama pull qwen2.5:1.5b`, or pull the model selected in `STUDYBUDDY_MODEL`.
- **Slow response or timeout:** the first response may take longer while the model loads. Retry, close other memory-heavy apps, or choose a smaller model available in Ollama.
- **PowerShell blocks environment activation:** activation is not required by the Windows commands above; they call the virtual environment's Python directly.

## Privacy

Prompts are sent to the local Ollama endpoint configured for the app; there is no hosted model API in this project. The first model download contacts Ollama's model registry. Avoid entering sensitive personal information into any AI application unless you understand its data handling.

## Project story

This is intentionally small: the goal is not to build another generic chatbot, but to make technical practice available whenever one college friend needs it.

## License

The application code is MIT licensed. The model is distributed under its own license; check the model's current terms before redistribution.