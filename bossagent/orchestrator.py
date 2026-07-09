from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .agents import AGENT_SPECS, build_agents
from .llm import LLMClient


TASK_AGENT_MAP = {
    "机会判断": ["opportunity", "strategy", "chief"],
    "项目决策": ["strategy", "opportunity", "chief"],
    "内容生成": ["content", "chief"],
    "销售跟进": ["sales", "chief"],
    "资料整理": ["document", "chief"],
    "情景推演": ["scenario", "strategy", "chief"],
    "数据分析": ["analytics", "chief"],
    "演练沙盘": ["analytics", "scenario", "strategy", "chief"],
    "综合任务": ["opportunity", "strategy", "scenario", "analytics", "content", "sales", "chief"],
}


@dataclass
class AgentRun:
    agent_key: str
    agent_name: str
    output: str


@dataclass
class RunResult:
    selected_agents: List[str]
    agent_outputs: List[AgentRun]
    final_report: str


class AgentOrchestrator:
    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.agents = build_agents(llm)

    def select_agents(self, task_type: str, user_goal: str, has_documents: bool = False) -> List[str]:
        selected = TASK_AGENT_MAP.get(task_type, ["chief"])
        if has_documents and "document" not in selected:
            selected = ["document"] + selected
        return selected

    def run(self, task_type: str, user_goal: str, document_context: str = "") -> RunResult:
        selected = self.select_agents(task_type, user_goal, has_documents=bool(document_context.strip()))
        specialist_keys = [key for key in selected if key != "chief"]

        outputs: List[AgentRun] = []
        rolling_context = document_context

        for key in specialist_keys:
            worker = self.agents[key]
            output = worker.run(user_goal, rolling_context)
            outputs.append(AgentRun(agent_key=key, agent_name=AGENT_SPECS[key].name, output=output))
            rolling_context += f"\n\n## {AGENT_SPECS[key].name} 输出\n{output}"

        final_report = self._run_chief(user_goal, task_type, outputs, document_context)
        outputs.append(AgentRun(agent_key="chief", agent_name=AGENT_SPECS["chief"].name, output=final_report))
        return RunResult(selected_agents=selected, agent_outputs=outputs, final_report=final_report)

    def _run_chief(
        self,
        user_goal: str,
        task_type: str,
        outputs: List[AgentRun],
        document_context: str = "",
    ) -> str:
        combined = "\n\n".join(f"## {item.agent_name}\n{item.output}" for item in outputs)
        prompt = f"""你现在扮演 {AGENT_SPECS['chief'].name}。

角色设定：{AGENT_SPECS['chief'].role}

任务类型：{task_type}
用户总目标：
{user_goal}

资料上下文：
{document_context or "无"}

专业 Agent 输出：
{combined or "暂无，需直接给出总控建议。"}

请输出一份完整 Markdown 报告，必须包含：
1. 执行摘要
2. 目标拆解
3. 各 AI 员工关键结论
4. 7 天最小行动计划
5. 所需资源
6. 风险、边界和人工确认事项
7. 下一步决策建议
"""
        return self.llm.complete(prompt).content


def crewai_available() -> bool:
    try:
        import crewai  # noqa: F401

        return True
    except Exception:
        return False
