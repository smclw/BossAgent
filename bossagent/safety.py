HIGH_RISK_KEYWORDS = [
    "自动发送",
    "自动付款",
    "自动下单",
    "自动删除",
    "自动修改",
    "绕过风控",
    "刷单",
    "爬取隐私",
    "盗取",
]


def safety_notice(user_goal: str) -> str:
    hits = [item for item in HIGH_RISK_KEYWORDS if item in user_goal]
    if not hits:
        return ""
    return (
        "检测到可能涉及高风险外部动作或敏感行为："
        + "、".join(hits)
        + "。BossAgent 第一版只提供建议和草案，不会自动执行外部操作；执行前必须人工确认。"
    )
