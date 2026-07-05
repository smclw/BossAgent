from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
UPLOAD_DIR = ROOT_DIR / "uploads"
EXPORT_DIR = ROOT_DIR / "exports"
MODEL_DIR = ROOT_DIR / "models"
ENV_PATH = ROOT_DIR / ".env"


@dataclass(frozen=True)
class AppConfig:
    llm_provider: str
    openai_api_key: str
    model_name: str
    api_base_url: str
    temperature: float
    use_mock_llm: bool
    local_model_dir: str
    local_context_window: int
    local_max_tokens: int
    local_gpu_layers: int
    local_chat_format: str

    @property
    def has_api_key(self) -> bool:
        return bool(self.openai_api_key.strip())

    @property
    def effective_provider(self) -> str:
        if self.use_mock_llm or self.llm_provider == "mock":
            return "mock"
        if self.llm_provider == "local-folder":
            return "local-folder"
        if not self.has_api_key:
            return "mock"
        return "openai-compatible"


def load_config() -> AppConfig:
    load_dotenv(ENV_PATH, override=True)

    return AppConfig(
        llm_provider=os.getenv("LLM_PROVIDER", "openai-compatible").strip(),
        openai_api_key=os.getenv("OPENAI_API_KEY", "").strip(),
        model_name=os.getenv("MODEL_NAME", "gpt-4.1-mini").strip(),
        api_base_url=os.getenv("API_BASE_URL", "https://api.openai.com/v1").strip(),
        temperature=float(os.getenv("TEMPERATURE", "0.4")),
        use_mock_llm=os.getenv("USE_MOCK_LLM", "false").lower() in {"1", "true", "yes", "on"},
        local_model_dir=os.getenv("LOCAL_MODEL_DIR", str(MODEL_DIR)).strip(),
        local_context_window=int(os.getenv("LOCAL_CONTEXT_WINDOW", "4096")),
        local_max_tokens=int(os.getenv("LOCAL_MAX_TOKENS", "1024")),
        local_gpu_layers=int(os.getenv("LOCAL_GPU_LAYERS", "0")),
        local_chat_format=os.getenv("LOCAL_CHAT_FORMAT", "").strip(),
    )


def ensure_runtime_dirs() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    UPLOAD_DIR.mkdir(exist_ok=True)
    EXPORT_DIR.mkdir(exist_ok=True)
    MODEL_DIR.mkdir(exist_ok=True)


def save_env_settings(values: dict[str, str]) -> None:
    existing: dict[str, str] = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.lstrip().startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            existing[key.strip()] = value.strip()

    existing.update({key: str(value) for key, value in values.items()})
    ordered_keys = [
        "LLM_PROVIDER",
        "OPENAI_API_KEY",
        "MODEL_NAME",
        "API_BASE_URL",
        "TEMPERATURE",
        "USE_MOCK_LLM",
        "LOCAL_MODEL_DIR",
        "LOCAL_CONTEXT_WINDOW",
        "LOCAL_MAX_TOKENS",
        "LOCAL_GPU_LAYERS",
        "LOCAL_CHAT_FORMAT",
    ]
    lines = ["# BossAgent local configuration", "# Do not commit real API keys.", ""]
    for key in ordered_keys:
        if key in existing:
            lines.append(f"{key}={existing[key]}")
    for key in sorted(set(existing) - set(ordered_keys)):
        lines.append(f"{key}={existing[key]}")
    ENV_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
