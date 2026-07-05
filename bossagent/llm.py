from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openai import OpenAI

from .config import AppConfig, ROOT_DIR


SYSTEM_PROMPT = """你是 BossAgent 的企业级 AI 员工系统。
要求：
1. 用中文输出，结构化、可执行、适合老板快速决策。
2. 不编造确定性事实；不确定处要标注为假设。
3. 不承诺违法、灰产、欺诈、刷量、侵犯隐私或高风险自动操作。
4. 所有删除、发送、支付、下单、修改外部系统的动作都必须要求人工确认。
5. 输出 Markdown。"""


_LOCAL_MODEL_CACHE: dict[str, Any] = {}


@dataclass
class LLMResult:
    content: str
    provider: str


class LLMClient:
    def __init__(self, config: AppConfig):
        self.config = config

    def complete(self, prompt: str, system_prompt: str = SYSTEM_PROMPT) -> LLMResult:
        provider = self.config.effective_provider
        if provider == "mock":
            return LLMResult(content=self._mock_response(prompt), provider="mock")
        if provider == "local-folder":
            return self._complete_with_local_model(prompt, system_prompt)
        return self._complete_with_openai_compatible(prompt, system_prompt)

    def _complete_with_openai_compatible(self, prompt: str, system_prompt: str) -> LLMResult:
        client = OpenAI(
            api_key=self.config.openai_api_key,
            base_url=self.config.api_base_url or None,
        )
        response = client.chat.completions.create(
            model=self.config.model_name,
            temperature=self.config.temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        return LLMResult(content=response.choices[0].message.content or "", provider="openai-compatible")

    def _complete_with_local_model(self, prompt: str, system_prompt: str) -> LLMResult:
        try:
            from llama_cpp import Llama
        except Exception as exc:
            return LLMResult(
                content=(
                    "## 本地模型未就绪\n\n"
                    "已选择“本地模型文件夹”模式，但当前环境没有安装 `llama-cpp-python`。\n\n"
                    "请先运行：\n\n"
                    "```powershell\n"
                    ".\\.venv\\Scripts\\python.exe -m pip install -r requirements-local.txt\n"
                    "```\n\n"
                    f"原始错误：`{exc}`"
                ),
                provider="local-folder-error",
            )

        model_path = self._find_local_gguf_model()
        if model_path is None:
            return LLMResult(
                content=(
                    "## 未找到本地模型文件\n\n"
                    f"请把 `.gguf` 模型文件放到：`{self.config.local_model_dir}`\n\n"
                    "BossAgent 会自动选择该文件夹内的第一个 `.gguf` 文件。"
                ),
                provider="local-folder-error",
            )

        cache_key = str(model_path.resolve())
        if cache_key not in _LOCAL_MODEL_CACHE:
            kwargs: dict[str, Any] = {
                "model_path": cache_key,
                "n_ctx": self.config.local_context_window,
                "n_gpu_layers": self.config.local_gpu_layers,
                "verbose": False,
            }
            if self.config.local_chat_format:
                kwargs["chat_format"] = self.config.local_chat_format
            _LOCAL_MODEL_CACHE[cache_key] = Llama(**kwargs)

        llm = _LOCAL_MODEL_CACHE[cache_key]
        response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=self.config.temperature,
            max_tokens=self.config.local_max_tokens,
        )
        content = response["choices"][0]["message"]["content"]
        return LLMResult(content=content, provider=f"local-folder:{model_path.name}")

    def _find_local_gguf_model(self) -> Path | None:
        model_dir = Path(self.config.local_model_dir).expanduser()
        if not model_dir.is_absolute():
            model_dir = ROOT_DIR / model_dir
        if model_dir.is_file() and model_dir.suffix.lower() == ".gguf":
            return model_dir
        if not model_dir.exists():
            return None
        candidates = sorted(model_dir.rglob("*.gguf"))
        return candidates[0] if candidates else None

    def _mock_response(self, prompt: str) -> str:
        title = "本地演示输出"
        if "时代机会雷达" in prompt:
            title = "机会雷达分析"
        elif "老板战略顾问" in prompt:
            title = "项目决策建议"
        elif "老板内容分身" in prompt:
            title = "内容分身草案"
        elif "销售跟进助手" in prompt:
            title = "销售跟进方案"
        elif "资料整理助手" in prompt:
            title = "资料整理摘要"
        elif "总裁办执行官" in prompt:
            title = "总控执行报告"

        return f"""## {title}

> 当前处于本地演示模式。配置 `.env` 中的 `OPENAI_API_KEY` 后，将调用真实模型；或在系统设置中选择“本地模型文件夹”加载 `.gguf` 模型。

### 核心判断
- 任务具备继续拆解和执行的价值，但需要先确认目标用户、预算、时间窗口和可调动资源。
- 第一版建议用小样本、低成本、强反馈的方式验证，不要一开始重资产投入。

### 可执行动作
1. 明确目标：把输入目标改写成一个 7 天内可验证的结果。
2. 找到样本：选择 5-10 个真实客户或资料样本做快速访谈/试跑。
3. 产出材料：形成一页纸方案、成交话术、行动清单和复盘表。
4. 人工确认：涉及发送、下单、付款、删除、外部系统修改的动作全部先人工确认。

### 风险提示
- 该输出是演示模板，不替代法律、财务、医疗或投资建议。
- 若要商业化，需要补充权限、日志、审计、企业数据隔离和人工审批流。
"""
