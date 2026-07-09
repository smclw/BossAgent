from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import streamlit as st

from bossagent.agents import AGENT_SPECS
from bossagent.analytics import chart_candidates, is_supported_data_file, load_dataframes, profile_datasets, profiles_to_markdown
from bossagent.config import MODEL_DIR, ROOT_DIR, UPLOAD_DIR, ensure_runtime_dirs, load_config, save_env_settings
from bossagent.documents import combine_texts, extract_text, is_supported_file
from bossagent.export import save_docx, save_markdown
from bossagent.llm import LLMClient
from bossagent.orchestrator import AgentOrchestrator, crewai_available
from bossagent.safety import safety_notice
from bossagent.simulation import build_drill_context
from bossagent.storage import get_task, init_db, list_tasks, save_task


st.set_page_config(page_title="BossAgent", page_icon="BA", layout="wide")


TASK_TYPES = ["机会判断", "项目决策", "情景推演", "数据分析", "演练沙盘", "内容生成", "销售跟进", "资料整理", "综合任务"]
PROVIDER_LABELS = {
    "mock": "本地演示模式",
    "openai-compatible": "OpenAI-compatible API",
    "local-folder": "本地模型文件夹（GGUF）",
}


def bootstrap() -> Tuple[LLMClient, AgentOrchestrator]:
    ensure_runtime_dirs()
    init_db()
    config = load_config()
    llm = LLMClient(config)
    return llm, AgentOrchestrator(llm)


def render_global_styles() -> None:
    st.markdown(
        """
<style>
:root {
    --ba-bg: #070A12;
    --ba-panel: rgba(14, 20, 35, 0.82);
    --ba-panel-strong: rgba(20, 31, 52, 0.92);
    --ba-border: rgba(106, 227, 255, 0.22);
    --ba-border-hot: rgba(65, 255, 177, 0.46);
    --ba-text: #F4F7FB;
    --ba-muted: #9CA9BE;
    --ba-cyan: #6AE3FF;
    --ba-green: #41FFB1;
    --ba-pink: #FF5DAF;
    --ba-yellow: #F5D76E;
}

.stApp {
    color: var(--ba-text);
    background:
        linear-gradient(180deg, rgba(7, 10, 18, 0.94), rgba(7, 10, 18, 0.98)),
        repeating-linear-gradient(90deg, rgba(106, 227, 255, 0.05) 0 1px, transparent 1px 72px),
        repeating-linear-gradient(0deg, rgba(65, 255, 177, 0.04) 0 1px, transparent 1px 72px),
        #070A12;
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background: linear-gradient(180deg, transparent 0%, rgba(106, 227, 255, 0.08) 50%, transparent 100%);
    animation: ba-scan 9s linear infinite;
    opacity: 0.35;
    z-index: 0;
}

.stApp::after {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background: repeating-linear-gradient(180deg, rgba(255,255,255,0.025) 0 1px, transparent 1px 5px);
    mix-blend-mode: screen;
    opacity: 0.18;
    z-index: 0;
}

@keyframes ba-scan {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100%); }
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(11, 18, 31, 0.98), rgba(7, 10, 18, 0.98));
    border-right: 1px solid var(--ba-border);
}

header[data-testid="stHeader"] {
    background: rgba(7, 10, 18, 0.72);
    border-bottom: 1px solid rgba(106, 227, 255, 0.12);
    backdrop-filter: blur(10px);
}

[data-testid="stToolbar"] {
    color: var(--ba-text);
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: var(--ba-text);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    position: relative;
    z-index: 1;
}

h1, h2, h3 {
    color: var(--ba-text);
    letter-spacing: 0;
}

p, li, label, span {
    color: inherit;
}

.ba-hero {
    position: relative;
    overflow: hidden;
    border: 1px solid var(--ba-border);
    background:
        linear-gradient(135deg, rgba(20, 31, 52, 0.94), rgba(9, 13, 24, 0.9)),
        repeating-linear-gradient(45deg, rgba(106, 227, 255, 0.06) 0 1px, transparent 1px 16px);
    border-radius: 18px;
    padding: 34px 34px 28px;
    box-shadow: 0 24px 80px rgba(0, 0, 0, 0.36), inset 0 0 0 1px rgba(255,255,255,0.04);
}

.ba-hero::before {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--ba-cyan), var(--ba-green), var(--ba-pink));
    animation: ba-pulse 3.8s ease-in-out infinite;
}

@keyframes ba-pulse {
    0%, 100% { opacity: 0.45; }
    50% { opacity: 1; }
}

.ba-kicker {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    color: var(--ba-green);
    border: 1px solid rgba(65, 255, 177, 0.28);
    background: rgba(65, 255, 177, 0.08);
    border-radius: 999px;
    padding: 6px 12px;
    font-size: 13px;
    font-weight: 700;
}

.ba-led {
    width: 8px;
    height: 8px;
    border-radius: 999px;
    background: var(--ba-green);
    box-shadow: 0 0 18px var(--ba-green);
}

.ba-hero h1 {
    font-size: 48px;
    line-height: 1.08;
    margin: 20px 0 14px;
}

.ba-hero p {
    max-width: 860px;
    color: #C8D3E5;
    font-size: 18px;
    line-height: 1.72;
}

.ba-command-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 22px;
}

.ba-chip {
    border: 1px solid rgba(106, 227, 255, 0.25);
    color: #D9F7FF;
    background: rgba(106, 227, 255, 0.08);
    border-radius: 999px;
    padding: 8px 12px;
    font-size: 13px;
}

.ba-grid {
    display: grid;
    gap: 14px;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    margin: 18px 0 8px;
}

.ba-card {
    border: 1px solid var(--ba-border);
    background: var(--ba-panel);
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 18px 48px rgba(0, 0, 0, 0.24);
    transition: border-color 180ms ease, transform 180ms ease, background 180ms ease;
}

.ba-card:hover {
    transform: translateY(-2px);
    border-color: var(--ba-border-hot);
    background: var(--ba-panel-strong);
}

.ba-card .ba-card-title {
    color: var(--ba-text);
    font-size: 17px;
    font-weight: 800;
    margin-bottom: 8px;
}

.ba-card .ba-card-meta {
    color: var(--ba-muted);
    font-size: 13px;
    line-height: 1.62;
}

.ba-stat {
    border-left: 3px solid var(--ba-cyan);
    background: rgba(106, 227, 255, 0.07);
}

.ba-stat strong {
    color: var(--ba-text);
    display: block;
    font-size: 24px;
    margin-bottom: 3px;
}

.ba-stat span {
    color: var(--ba-muted);
    font-size: 13px;
}

.ba-section-title {
    margin: 28px 0 10px;
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--ba-text);
}

.ba-section-title::before {
    content: "";
    width: 28px;
    height: 2px;
    background: linear-gradient(90deg, var(--ba-cyan), var(--ba-green));
    box-shadow: 0 0 14px rgba(106, 227, 255, 0.8);
}

.ba-agent-line {
    display: grid;
    grid-template-columns: 140px 1fr;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid rgba(106, 227, 255, 0.12);
}

.ba-agent-line:last-child {
    border-bottom: 0;
}

.ba-agent-name {
    color: var(--ba-green);
    font-weight: 800;
}

.ba-agent-role {
    color: #C8D3E5;
}

.ba-run-panel {
    border: 1px solid rgba(65, 255, 177, 0.25);
    background: linear-gradient(135deg, rgba(65, 255, 177, 0.08), rgba(106, 227, 255, 0.06));
    border-radius: 14px;
    padding: 16px;
}

.ba-sidebar-brand {
    border: 1px solid var(--ba-border);
    border-radius: 14px;
    padding: 16px;
    background: rgba(106, 227, 255, 0.06);
    margin-bottom: 14px;
}

.ba-sidebar-brand strong {
    display: block;
    font-size: 22px;
    color: var(--ba-text);
}

.ba-sidebar-brand span {
    color: var(--ba-muted);
    font-size: 12px;
}

.ba-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(106, 227, 255, 0.45), transparent);
    margin: 22px 0;
}

.stButton > button,
.stDownloadButton > button,
[data-testid="stFormSubmitButton"] button {
    border: 1px solid rgba(65, 255, 177, 0.45) !important;
    background: linear-gradient(90deg, rgba(16, 170, 210, 0.95), rgba(24, 201, 139, 0.95)) !important;
    color: #041015 !important;
    font-weight: 800 !important;
    border-radius: 10px !important;
    box-shadow: 0 12px 32px rgba(65, 255, 177, 0.18);
}

.stTextArea textarea,
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(8, 13, 24, 0.92) !important;
    color: var(--ba-text) !important;
    border-color: rgba(106, 227, 255, 0.24) !important;
    border-radius: 10px !important;
}

[data-testid="stMetric"] {
    border: 1px solid var(--ba-border);
    border-radius: 14px;
    padding: 14px;
    background: var(--ba-panel);
}

[data-testid="stExpander"] {
    border: 1px solid rgba(106, 227, 255, 0.2);
    background: rgba(12, 18, 31, 0.78);
    border-radius: 12px;
}

@media (max-width: 760px) {
    .ba-hero { padding: 24px 20px; }
    .ba-hero h1 { font-size: 34px; }
    .ba-agent-line { grid-template-columns: 1fr; }
}
</style>
""",
        unsafe_allow_html=True,
    )


def render_sidebar() -> str:
    st.sidebar.markdown(
        """
<div class="ba-sidebar-brand">
  <strong>BossAgent</strong>
  <span>AI Workforce Control Deck</span>
</div>
""",
        unsafe_allow_html=True,
    )
    render_sidebar_model_launcher()
    return st.sidebar.radio("菜单", ["首页", "新建任务", "上传资料", "数据分析", "演练沙盘", "历史任务", "系统设置"])


def render_sidebar_model_launcher() -> None:
    config = load_config()
    provider_keys = list(PROVIDER_LABELS.keys())
    current_provider = config.effective_provider
    provider_index = provider_keys.index(current_provider) if current_provider in provider_keys else 0

    with st.sidebar.expander("模型启动方式", expanded=False):
        st.caption(f"当前：{PROVIDER_LABELS.get(config.effective_provider, config.effective_provider)}")
        selected_label = st.selectbox(
            "选择模型模式",
            list(PROVIDER_LABELS.values()),
            index=provider_index,
            key="sidebar_provider",
        )
        selected_provider = next(key for key, value in PROVIDER_LABELS.items() if value == selected_label)

        model_name = config.model_name
        api_base_url = config.api_base_url
        openai_api_key = config.openai_api_key
        local_model_dir = config.local_model_dir or str(MODEL_DIR)

        if selected_provider == "openai-compatible":
            model_name = st.text_input("模型名称", value=config.model_name, key="sidebar_model_name")
            api_base_url = st.text_input("API Base URL", value=config.api_base_url, key="sidebar_api_base")
            openai_api_key = st.text_input("API Key", value=config.openai_api_key, type="password", key="sidebar_api_key")
        elif selected_provider == "local-folder":
            local_model_dir = st.text_input("GGUF 模型目录", value=local_model_dir, key="sidebar_local_dir")
            st.caption("把 .gguf 模型放进 models/，或填写完整 .gguf 文件路径。")
        else:
            st.caption("无需 API Key，适合演示 UI 和流程。")

        if st.button("应用模型设置", use_container_width=True):
            save_env_settings(
                {
                    "LLM_PROVIDER": selected_provider,
                    "OPENAI_API_KEY": openai_api_key,
                    "MODEL_NAME": model_name,
                    "API_BASE_URL": api_base_url,
                    "TEMPERATURE": str(config.temperature),
                    "USE_MOCK_LLM": "true" if selected_provider == "mock" else "false",
                    "LOCAL_MODEL_DIR": local_model_dir,
                    "LOCAL_CONTEXT_WINDOW": str(config.local_context_window),
                    "LOCAL_MAX_TOKENS": str(config.local_max_tokens),
                    "LOCAL_GPU_LAYERS": str(config.local_gpu_layers),
                    "LOCAL_CHAT_FORMAT": config.local_chat_format,
                }
            )
            st.success("已保存，正在重载。")
            st.rerun()


def page_heading(kicker: str, title: str, body: str) -> None:
    st.markdown(
        f"""
<div class="ba-hero">
  <div class="ba-kicker"><span class="ba-led"></span>{kicker}</div>
  <h1>{title}</h1>
  <p>{body}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def section_title(title: str) -> None:
    st.markdown(f'<h3 class="ba-section-title">{title}</h3>', unsafe_allow_html=True)


def card_grid(cards: List[Tuple[str, str]]) -> None:
    html = ['<div class="ba-grid">']
    for title, body in cards:
        html.append(
            f"""
<div class="ba-card">
  <div class="ba-card-title">{title}</div>
  <div class="ba-card-meta">{body}</div>
</div>
"""
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def stat_grid(stats: List[Tuple[str, str]]) -> None:
    html = ['<div class="ba-grid">']
    for value, label in stats:
        html.append(f'<div class="ba-card ba-stat"><strong>{value}</strong><span>{label}</span></div>')
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def save_uploaded_files(files) -> Tuple[List[str], str]:
    saved_names: List[str] = []
    extracted_texts: List[str] = []

    for uploaded_file in files:
        if not is_supported_file(uploaded_file.name):
            st.warning(f"暂不支持文件类型：{uploaded_file.name}")
            continue
        target = UPLOAD_DIR / uploaded_file.name
        target.write_bytes(uploaded_file.getbuffer())
        saved_names.append(uploaded_file.name)
        try:
            extracted_texts.append(f"## 文件：{uploaded_file.name}\n{extract_text(target)}")
        except Exception as exc:
            st.error(f"{uploaded_file.name} 解析失败：{exc}")

    return saved_names, combine_texts(extracted_texts)


def save_uploaded_data_files(files) -> Tuple[List[str], List[Path]]:
    saved_names: List[str] = []
    saved_paths: List[Path] = []

    for uploaded_file in files:
        if not is_supported_data_file(uploaded_file.name):
            st.warning(f"暂不支持数据文件类型：{uploaded_file.name}")
            continue
        safe_name = Path(uploaded_file.name).name
        target = UPLOAD_DIR / safe_name
        target.write_bytes(uploaded_file.getbuffer())
        saved_names.append(safe_name)
        saved_paths.append(target)

    return saved_names, saved_paths


def render_home() -> None:
    page_heading(
        "24 小时 AI 员工中控台",
        "BossAgent：给老板配置一组 AI 员工。",
        "输入一个目标或上传资料后，系统会调度机会雷达、战略顾问、内容分身、销售跟进、资料整理和总裁办执行官，协作产出一份可执行报告。",
    )

    stat_grid(
        [
            ("8", "内置 AI 员工"),
            ("Drill Lab", "MiroFish x Data Analytics 演练沙盘"),
            ("Local-first", "本地运行与本地存储"),
            ("OpenAI-compatible", "兼容云端与本地模型服务"),
            ("MD / DOCX", "报告导出格式"),
        ]
    )

    section_title("AI 员工矩阵")
    cards = [
        (spec.title, f"{spec.name}<br>{spec.goal}")
        for spec in AGENT_SPECS.values()
    ]
    card_grid(cards)

    section_title("任务流水线")
    st.markdown(
        """
<div class="ba-card">
  <div class="ba-agent-line"><div class="ba-agent-name">01 输入目标</div><div class="ba-agent-role">把老板的业务问题、项目想法、客户情况或资料需求输入系统。</div></div>
  <div class="ba-agent-line"><div class="ba-agent-name">02 分配员工</div><div class="ba-agent-role">执行总控根据任务类型选择对应 Agent，必要时加入资料整理助手。</div></div>
  <div class="ba-agent-line"><div class="ba-agent-name">03 协作分析</div><div class="ba-agent-role">各 Agent 输出专业结论；情景推演借鉴 MiroFish 多角色模拟，数据分析借鉴 Data Analytics 工作流。</div></div>
  <div class="ba-agent-line"><div class="ba-agent-name">04 生成报告</div><div class="ba-agent-role">保存历史记录，支持 Markdown 与 DOCX 下载，便于复盘和分享。</div></div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_new_task(orchestrator: AgentOrchestrator) -> None:
    page_heading(
        "Mission Control",
        "新建任务",
        "把目标交给 BossAgent，选择任务类型后启动 AI 分身协作。每个 Agent 的输出会保留过程，最后由总控生成完整报告。",
    )

    left, right = st.columns([1.35, 0.9])
    with left:
        task_goal = st.text_area(
            "输入任务目标",
            height=190,
            placeholder="例如：我想判断 AI 员工配置服务是否值得做，并生成首批销售话术。",
        )
        task_type = st.selectbox("选择任务类型", TASK_TYPES)
        uploaded_files = st.file_uploader(
            "可选：上传补充资料",
            type=["pdf", "docx", "xlsx", "xls", "csv", "txt"],
            accept_multiple_files=True,
        )

        launch = st.button("启动 AI 分身", type="primary", use_container_width=True)

    with right:
        selected = orchestrator.select_agents(task_type, task_goal, has_documents=bool(uploaded_files))
        st.markdown('<div class="ba-run-panel">', unsafe_allow_html=True)
        st.markdown("#### 即将调度")
        for key in selected:
            spec = AGENT_SPECS[key]
            st.markdown(f"- **{spec.title}** `{spec.name}`")
        st.markdown("</div>", unsafe_allow_html=True)

    if launch:
        if not task_goal.strip() and not uploaded_files:
            st.error("请先输入任务目标或上传资料。")
            return

        warning = safety_notice(task_goal)
        if warning:
            st.warning(warning)

        progress = st.progress(0, text="正在启动 AI 员工...")
        with st.spinner("AI 员工正在协作..."):
            saved_files, document_context = save_uploaded_files(uploaded_files or [])
            progress.progress(30, text="资料与任务上下文已准备")
            result = orchestrator.run(task_type, task_goal or "请整理上传资料并输出行动建议。", document_context)
            progress.progress(82, text="总裁办执行官正在汇总报告")
            task_id = save_task(task_type, task_goal, saved_files, result.agent_outputs, result.final_report)
            progress.progress(100, text="任务完成")

        st.success(f"任务完成，已保存为历史任务 #{task_id}")
        render_agent_outputs(result.agent_outputs)
        render_downloads(result.final_report)


def render_upload(orchestrator: AgentOrchestrator) -> None:
    page_heading(
        "Document Intelligence",
        "上传资料",
        "把 PDF、Word、Excel、CSV 或 TXT 交给资料整理助手。系统只读取文本，不执行文件里的任何代码。",
    )

    files = st.file_uploader(
        "上传 PDF、Word、Excel、CSV、TXT",
        type=["pdf", "docx", "xlsx", "xls", "csv", "txt"],
        accept_multiple_files=True,
    )
    note = st.text_area("补充说明", placeholder="例如：请重点提炼客户需求、报价信息和下一步行动。")

    card_grid(
        [
            ("安全读取", "只做文本提取，不运行宏、脚本或未知代码。"),
            ("行动导向", "输出重点摘要、行动清单、结构化信息。"),
            ("可追溯", "整理结果会保存到历史任务，方便复盘。"),
        ]
    )

    if st.button("自动摘要和提炼行动清单", type="primary", use_container_width=True):
        if not files:
            st.error("请先上传至少一个文件。")
            return
        with st.spinner("资料整理助手正在读取文件..."):
            saved_files, document_context = save_uploaded_files(files)
            goal = note or "请整理上传资料，输出重点摘要、行动清单和表格化信息。"
            result = orchestrator.run("资料整理", goal, document_context)
            task_id = save_task("资料整理", goal, saved_files, result.agent_outputs, result.final_report)

        st.success(f"资料整理完成，已保存为历史任务 #{task_id}")
        render_agent_outputs(result.agent_outputs)
        render_downloads(result.final_report)


def render_data_analytics(orchestrator: AgentOrchestrator) -> None:
    page_heading(
        "Data Analytics Lab",
        "数据分析",
        "上传 CSV 或 Excel 后，BossAgent 会先做本地数据画像、质量检查和图表预览，再调用数据分析师与总控生成经营分析报告。",
    )

    files = st.file_uploader(
        "上传 CSV、Excel",
        type=["csv", "xlsx", "xls"],
        accept_multiple_files=True,
        key="analytics_files",
    )
    goal = st.text_area(
        "分析目标",
        height=120,
        placeholder="例如：请分析销售数据的增长机会、异常客户、重点渠道和下一步动作。",
    )

    card_grid(
        [
            ("本地读取", "表格文件只在本地解析，不执行任何上传文件中的代码。"),
            ("数据画像", "自动输出字段、缺失值、数值摘要、高频类别和预览表。"),
            ("AI 报告", "把数据画像交给 DataAnalyticsAgent，生成经营洞察和下一步分析建议。"),
        ]
    )

    if st.button("启动数据分析", type="primary", use_container_width=True):
        if not files:
            st.error("请先上传至少一个 CSV 或 Excel 文件。")
            return

        with st.spinner("正在读取数据并生成画像..."):
            saved_files, saved_paths = save_uploaded_data_files(files)
            datasets = load_dataframes(saved_paths)
            if not datasets:
                st.error("没有读取到可分析的数据表。")
                return
            profiles = profile_datasets(datasets)
            analytics_context = profiles_to_markdown(profiles, goal)

        section_title("数据画像")
        for profile in profiles:
            with st.expander(f"{profile.file_name} / {profile.sheet_name}", expanded=True):
                st.write(f"行数：{profile.rows}，列数：{profile.columns}")
                st.markdown("**字段**：" + "、".join(profile.column_names))
                st.markdown("**缺失值**")
                st.write(profile.missing_summary or "未检测到缺失值。")
                st.markdown("**数据预览**")
                st.markdown(profile.preview_markdown)

        section_title("图表预览")
        chart_sets = chart_candidates(datasets)
        rendered_chart = False
        for dataset_name, charts in chart_sets.items():
            for chart_title, chart_df in charts.items():
                if chart_df.empty:
                    continue
                st.markdown(f"**{dataset_name} | {chart_title}**")
                st.bar_chart(chart_df)
                rendered_chart = True
                break
            if rendered_chart:
                break
        if not rendered_chart:
            st.info("暂未检测到适合直接绘制的数值或类别字段。")

        with st.spinner("DataAnalyticsAgent 正在生成分析报告..."):
            result = orchestrator.run("数据分析", goal or "请基于上传数据输出经营洞察、风险和下一步动作。", analytics_context)
            task_id = save_task("数据分析", goal, saved_files, result.agent_outputs, result.final_report)

        st.success(f"数据分析完成，已保存为历史任务 #{task_id}")
        render_agent_outputs(result.agent_outputs)
        render_downloads(result.final_report)


def render_drill_lab(orchestrator: AgentOrchestrator) -> None:
    page_heading(
        "MiroFish x Data Analytics",
        "演练沙盘",
        "把真实表格数据变成演练证据，再用多角色模拟推演客户、竞品、渠道、交付和舆论反应，输出一份老板决策沙盘报告。",
    )

    left, right = st.columns([1.2, 0.8])
    with left:
        scenario = st.text_area(
            "演练主题",
            height=150,
            placeholder="例如：我们准备推出 9999 元/年的 BossAgent 企业服务，请基于销售数据推演客户反应、竞品动作和成交路径。",
        )
        drill_type = st.selectbox(
            "演练类型",
            ["新品发布", "销售成交", "价格调整", "渠道招商", "舆论传播", "组织变革", "投资决策"],
        )
        rounds = st.slider("推演轮次", min_value=2, max_value=5, value=3, step=1)
        files = st.file_uploader(
            "可选：上传 CSV、Excel 作为演练证据",
            type=["csv", "xlsx", "xls"],
            accept_multiple_files=True,
            key="drill_files",
        )
        launch = st.button("启动演练沙盘", type="primary", use_container_width=True)

    with right:
        card_grid(
            [
                ("Data Analytics 层", "读取 CSV / Excel，生成字段、缺失值、数值摘要、类别分布和图表预览。"),
                ("MiroFish 推演层", "模拟多类角色的初始反应、相互影响、态度变化和扩散路径。"),
                ("BossAgent 总控层", "把数据证据、角色推演和战略建议汇总成 Markdown / DOCX 报告。"),
            ]
        )

    if launch:
        if not scenario.strip() and not files:
            st.error("请先填写演练主题，或上传一份可分析的数据。")
            return

        warning = safety_notice(scenario)
        if warning:
            st.warning(warning)

        saved_files: List[str] = []
        analytics_context = ""
        datasets = {}
        profiles = []

        if files:
            with st.spinner("正在读取数据并生成 Data Analytics 画像..."):
                saved_files, saved_paths = save_uploaded_data_files(files)
                datasets = load_dataframes(saved_paths)
                profiles = profile_datasets(datasets)
                analytics_context = profiles_to_markdown(profiles, scenario)

            section_title("Data Analytics 画像")
            for profile in profiles:
                with st.expander(f"{profile.file_name} / {profile.sheet_name}", expanded=True):
                    st.write(f"行数：{profile.rows}，列数：{profile.columns}")
                    st.markdown("**字段**：" + "、".join(profile.column_names))
                    st.markdown("**缺失值**")
                    st.write(profile.missing_summary or "未检测到缺失值。")
                    st.markdown("**数据预览**")
                    st.markdown(profile.preview_markdown)

            section_title("演练证据图表")
            chart_sets = chart_candidates(datasets)
            chart_count = 0
            for dataset_name, charts in chart_sets.items():
                for chart_title, chart_df in charts.items():
                    if chart_df.empty:
                        continue
                    st.markdown(f"**{dataset_name} | {chart_title}**")
                    st.bar_chart(chart_df)
                    chart_count += 1
                    if chart_count >= 2:
                        break
                if chart_count >= 2:
                    break
            if chart_count == 0:
                st.info("暂未检测到适合直接绘制的数值或类别字段。")

        drill_goal = f"演练类型：{drill_type}\n演练主题：{scenario or '请基于上传数据提出业务演练主题。'}"
        drill_context = build_drill_context(drill_goal, analytics_context, rounds=rounds)

        with st.spinner("演练沙盘正在运行：数据分析师 -> MiroFish 沙盘推演 -> 战略顾问 -> 总控..."):
            result = orchestrator.run("演练沙盘", drill_goal, drill_context)
            task_id = save_task("演练沙盘", drill_goal, saved_files, result.agent_outputs, result.final_report)

        st.success(f"演练完成，已保存为历史任务 #{task_id}")
        render_agent_outputs(result.agent_outputs)
        render_downloads(result.final_report)


def render_history() -> None:
    page_heading(
        "Task Memory",
        "历史任务",
        "所有任务记录、Agent 输出和最终报告都会保存在本地 SQLite，便于回看、复盘和再次加工。",
    )
    tasks = list_tasks()
    if not tasks:
        st.info("还没有历史任务。")
        return

    stat_grid([(str(len(tasks)), "本地历史任务")])
    labels = [f"#{item['id']} | {item['created_at']} | {item['task_type']} | {item['user_goal'][:40]}" for item in tasks]
    selected = st.selectbox("选择任务", labels)
    task_id = int(selected.split("|")[0].replace("#", "").strip())
    task = get_task(task_id)
    if task is None:
        st.error("任务不存在。")
        return

    st.caption(f"创建时间：{task['created_at']}  |  类型：{task['task_type']}")
    st.write("目标：", task["user_goal"] or "未填写")
    if task["uploaded_files"]:
        st.write("上传文件：", "、".join(task["uploaded_files"]))

    with st.expander("Agent 输出", expanded=False):
        for item in task["agent_outputs"]:
            st.markdown(f"### {item['agent_name']}")
            st.markdown(item["output"])

    section_title("最终报告")
    st.markdown(task["final_report"])
    render_downloads(task["final_report"])


def render_settings() -> None:
    page_heading(
        "Model Console",
        "系统设置",
        "在这里选择云端模型、本地 OpenAI-compatible 服务，或直接加载本地 GGUF 模型文件夹。",
    )
    config = load_config()

    provider_keys = list(PROVIDER_LABELS.keys())
    current_provider = config.effective_provider
    provider_index = provider_keys.index(current_provider) if current_provider in provider_keys else 0

    stat_grid(
        [
            (PROVIDER_LABELS.get(config.effective_provider, config.effective_provider), "当前调用模式"),
            ("已配置" if config.has_api_key else "未配置", "API Key 状态"),
            ("已安装" if crewai_available() else "内置编排器", "CrewAI 状态"),
        ]
    )

    with st.form("settings_form"):
        selected_label = st.selectbox("模型接口", list(PROVIDER_LABELS.values()), index=provider_index)
        selected_provider = next(key for key, value in PROVIDER_LABELS.items() if value == selected_label)

        section_title("OpenAI-compatible API")
        model_name = st.text_input("模型名称", value=config.model_name)
        api_base_url = st.text_input("API Base URL", value=config.api_base_url)
        openai_api_key = st.text_input("API Key", value=config.openai_api_key, type="password")
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.5, value=float(config.temperature), step=0.1)

        section_title("本地模型文件夹")
        local_model_dir = st.text_input("本地模型目录或 GGUF 文件路径", value=config.local_model_dir or str(MODEL_DIR))
        local_context_window = st.number_input("上下文窗口", min_value=1024, max_value=32768, value=config.local_context_window, step=512)
        local_max_tokens = st.number_input("单次最大输出 Tokens", min_value=128, max_value=8192, value=config.local_max_tokens, step=128)
        local_gpu_layers = st.number_input("GPU Layers（CPU 可填 0）", min_value=0, max_value=200, value=config.local_gpu_layers, step=1)
        local_chat_format = st.text_input("Chat Format（可选，例如 chatml / llama-2）", value=config.local_chat_format)

        submitted = st.form_submit_button("保存设置", type="primary", use_container_width=True)

    if submitted:
        save_env_settings(
            {
                "LLM_PROVIDER": selected_provider,
                "OPENAI_API_KEY": openai_api_key,
                "MODEL_NAME": model_name,
                "API_BASE_URL": api_base_url,
                "TEMPERATURE": str(temperature),
                "USE_MOCK_LLM": "true" if selected_provider == "mock" else "false",
                "LOCAL_MODEL_DIR": local_model_dir,
                "LOCAL_CONTEXT_WINDOW": str(local_context_window),
                "LOCAL_MAX_TOKENS": str(local_max_tokens),
                "LOCAL_GPU_LAYERS": str(local_gpu_layers),
                "LOCAL_CHAT_FORMAT": local_chat_format,
            }
        )
        st.success("设置已保存到 .env，正在刷新配置。")
        st.rerun()

    render_local_model_status(config.local_model_dir)


def render_local_model_status(local_model_dir: str) -> None:
    section_title("本地模型检测")
    model_path = Path(local_model_dir).expanduser()
    if not model_path.is_absolute():
        model_path = ROOT_DIR / model_path

    if model_path.is_file() and model_path.suffix.lower() == ".gguf":
        st.success(f"已检测到 GGUF 模型文件：{model_path}")
        return

    if not model_path.exists():
        st.info(f"模型目录不存在，首次运行已准备默认目录：{MODEL_DIR}")
        return

    candidates = sorted(model_path.rglob("*.gguf"))
    if candidates:
        st.success(f"检测到 {len(candidates)} 个 GGUF 模型，默认使用：{candidates[0].name}")
        st.caption(str(candidates[0]))
    else:
        st.warning("暂未检测到 .gguf 模型文件。请把下载好的 GGUF 模型放入本地模型目录。")


def render_agent_outputs(agent_outputs) -> None:
    section_title("AI 员工输出过程")
    for item in agent_outputs:
        title = AGENT_SPECS.get(item.agent_key).title if item.agent_key in AGENT_SPECS else item.agent_name
        with st.expander(f"{title} | {item.agent_name}", expanded=item.agent_key == "chief"):
            st.markdown(item.output)

    section_title("最终报告")
    st.markdown(agent_outputs[-1].output)


def render_downloads(report: str) -> None:
    md_path = save_markdown(report)
    docx_path = save_docx(report)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "下载 Markdown 报告",
            data=md_path.read_bytes(),
            file_name=md_path.name,
            mime="text/markdown",
            use_container_width=True,
        )
    with col2:
        st.download_button(
            "下载 DOCX 报告",
            data=docx_path.read_bytes(),
            file_name=docx_path.name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )


def main() -> None:
    render_global_styles()
    _, orchestrator = bootstrap()
    page = render_sidebar()

    if page == "首页":
        render_home()
    elif page == "新建任务":
        render_new_task(orchestrator)
    elif page == "上传资料":
        render_upload(orchestrator)
    elif page == "数据分析":
        render_data_analytics(orchestrator)
    elif page == "演练沙盘":
        render_drill_lab(orchestrator)
    elif page == "历史任务":
        render_history()
    elif page == "系统设置":
        render_settings()


if __name__ == "__main__":
    main()
