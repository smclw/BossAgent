# Quick Start

## Requirements

- Python 3.10 or newer.
- Windows, macOS, or Linux.
- Optional: an OpenAI-compatible model API key.

## Clone

```bash
git clone https://github.com/smclw/BossAgent.git
cd BossAgent
```

## Create a Virtual Environment

```bash
python -m venv .venv
```

## Install Dependencies

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Configure Environment

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

Start with mock mode if you do not have an API key.

## Run

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

macOS / Linux:

```bash
streamlit run app.py
```

## First Run Example

1. Open the local Streamlit URL.
2. Go to New Task.
3. Choose Comprehensive Task.
4. Enter: "Evaluate whether an AI employee configuration service is worth launching."
5. Start the AI workforce.

## Run on Google Colab

Colab is useful for quick demos when you do not want to set up Python locally. Use mock mode first, and do not upload private data to a shared notebook.

### Clone and Install

```python
!git clone https://github.com/smclw/BossAgent.git
%cd BossAgent
!pip -q install -r requirements.txt
!cp .env.example .env
```

### Start Streamlit

```python
!printf "\\nLLM_PROVIDER=mock\\nUSE_MOCK_LLM=true\\n" >> .env
!streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &
```

### Create a Temporary Public URL

```python
!wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
!chmod +x cloudflared
!./cloudflared tunnel --url http://localhost:8501
```

Open the generated `trycloudflare.com` URL.

### Optional API Key

Use Colab Secrets:

```python
from google.colab import userdata
api_key = userdata.get("OPENAI_API_KEY")

from pathlib import Path
env_path = Path(".env")
text = env_path.read_text()
text += f"\\nLLM_PROVIDER=openai-compatible\\nUSE_MOCK_LLM=false\\nOPENAI_API_KEY={api_key}\\n"
env_path.write_text(text)
```

## Common Issues

### PowerShell blocks Activate.ps1

Use the Python executable directly, or run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### No API key

Use mock mode:

```env
LLM_PROVIDER=mock
USE_MOCK_LLM=true
```

### Local GGUF model mode

Install optional dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-local.txt
```
