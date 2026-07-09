from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class DrillRole:
    name: str
    stance: str
    concern: str


DEFAULT_DRILL_ROLES: List[DrillRole] = [
    DrillRole("核心客户", "关注价值、价格、信任和交付稳定性", "会不会真的解决我的问题"),
    DrillRole("观望客户", "容易被案例、口碑和风险提示影响", "现在买是不是太早"),
    DrillRole("销售负责人", "关注线索质量、成交路径和报价空间", "怎么更快推进成交"),
    DrillRole("交付负责人", "关注资源、人力、SOP 和服务边界", "承诺会不会超过交付能力"),
    DrillRole("竞品", "关注差异化、价格战和渠道拦截", "如何削弱 BossAgent 的优势"),
    DrillRole("渠道伙伴", "关注分润、转介绍难度和客户成功率", "值不值得帮忙推荐"),
    DrillRole("投资人/老板", "关注增长弹性、现金流和可复制性", "这是不是一门能规模化的生意"),
    DrillRole("公众舆论", "关注故事性、争议点和传播钩子", "这件事会被怎样理解和转发"),
]


def build_drill_context(
    scenario: str,
    analytics_context: str = "",
    roles: Iterable[DrillRole] = DEFAULT_DRILL_ROLES,
    rounds: int = 3,
) -> str:
    role_lines = "\n".join(
        f"- {role.name}：立场={role.stance}；核心疑问={role.concern}" for role in roles
    )
    data_section = analytics_context.strip() or "本次未上传结构化数据，请基于用户输入做定性推演，并明确标注为假设。"
    return f"""# BossAgent 演练沙盘上下文

## 演练主题
{scenario.strip() or "未填写具体主题，请围绕用户目标做通用业务演练。"}

## Data Analytics 数据画像
{data_section}

## MiroFish 风格角色池
{role_lines}

## 演练规则
- 这是本地 MVP 的轻量化推演，不代表真实社会预测或投资建议。
- 先用数据画像提取 3-5 个关键事实或信号。
- 再模拟 {rounds} 轮角色反应：初始反应、相互影响、最终态度变化。
- 每轮都要说明触发因素、主要分歧、可能扩散路径和风险。
- 不确定处必须标注为假设。
- 涉及删除、发送、支付、下单、修改外部系统的动作都必须人工确认。
"""
