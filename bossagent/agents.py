from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .llm import LLMClient


@dataclass(frozen=True)
class AgentSpec:
    key: str
    name: str
    title: str
    role: str
    goal: str
    output_requirements: List[str]


AGENT_SPECS: Dict[str, AgentSpec] = {
    "opportunity": AgentSpec(
        key="opportunity",
        name="OpportunityRadarAgent",
        title="机会雷达",
        role="时代机会雷达，擅长发现高势能行业、早期趋势、圈层机会和高弹性增长路径。",
        goal="判断一个行业、项目或关键词背后的机会窗口和进入方式。",
        output_requirements=["时代趋势", "进入窗口", "增长弹性", "关键资源", "风险点", "第一步行动"],
    ),
    "strategy": AgentSpec(
        key="strategy",
        name="StrategyAdvisorAgent",
        title="战略顾问",
        role="老板战略顾问，擅长判断项目值不值得做、怎么切入、怎么用最小成本试错。",
        goal="给出是否值得进入、投入产出、最小试错和退出条件。",
        output_requirements=["是否值得进入", "为什么", "投入产出", "最小试错方案", "退出条件"],
    ),
    "content": AgentSpec(
        key="content",
        name="ContentCloneAgent",
        title="内容分身",
        role="老板内容分身，擅长生成朋友圈、小红书、短视频、直播话术。",
        goal="根据用户定位和目标，生成可直接改写使用的内容素材。",
        output_requirements=["朋友圈文案", "小红书文案", "短视频脚本", "直播话术"],
    ),
    "sales": AgentSpec(
        key="sales",
        name="SalesFollowupAgent",
        title="销售跟进",
        role="销售跟进助手，擅长客户分层、成交话术、报价沟通、复购提醒。",
        goal="为客户沟通、报价、成交推进和复购设计行动话术。",
        output_requirements=["跟进话术", "报价沟通话术", "成交推进方案", "客户分层建议"],
    ),
    "document": AgentSpec(
        key="document",
        name="DocumentAnalystAgent",
        title="资料整理",
        role="资料整理助手，擅长读取文件、提炼重点、生成摘要和行动清单。",
        goal="从资料文本中提炼重点、摘要、行动清单和表格化信息。",
        output_requirements=["重点提炼", "摘要", "行动清单", "表格化信息"],
    ),
    "chief": AgentSpec(
        key="chief",
        name="ChiefOfStaffAgent",
        title="总裁办执行官",
        role="总裁办执行官，负责拆解任务、协调其他 Agent、汇总最终报告。",
        goal="把多个专业 Agent 的结果汇总成完整、可执行的老板报告。",
        output_requirements=["任务拆解", "各 Agent 结论", "优先级", "执行路线图", "风险与人工确认事项"],
    ),
}


class BossAgentWorker:
    def __init__(self, spec: AgentSpec, llm: LLMClient):
        self.spec = spec
        self.llm = llm

    def run(self, user_input: str, context: str = "") -> str:
        output_items = "\n".join(f"- {item}" for item in self.spec.output_requirements)
        prompt = f"""你现在扮演 {self.spec.name}。

角色设定：{self.spec.role}
目标：{self.spec.goal}

用户输入：
{user_input}

补充上下文：
{context or "无"}

请按以下栏目输出：
{output_items}

输出要求：
- Markdown 格式。
- 观点要明确，建议要可执行。
- 标注关键假设。
- 高风险外部动作必须提示人工确认。
"""
        return self.llm.complete(prompt).content


def build_agents(llm: LLMClient) -> Dict[str, BossAgentWorker]:
    return {key: BossAgentWorker(spec, llm) for key, spec in AGENT_SPECS.items()}
