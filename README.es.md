# BossAgent

**El AI Workforce OS para fundadores, operadores y equipos ambiciosos.**

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · Español · [Português](README.pt-BR.md) · [Français](README.fr.md)

BossAgent es un espacio de trabajo local-first y extensible para AI Agents. El usuario introduce un objetivo o sube documentos, y un equipo coordinado de empleados AI ayuda con investigación, planificación, redacción, análisis, seguimiento comercial, organización de documentos y reportes ejecutivos.

## Core Agents

| Agent | Status | Role |
| --- | --- | --- |
| Chief of Staff Agent | Available | Divide tareas, coordina agentes y resume el reporte final. |
| Opportunity Radar Agent | Available | Detecta tendencias, oportunidades, ventanas de mercado y riesgos. |
| Strategy Advisor Agent | Available | Evalúa si un proyecto vale la pena y diseña pruebas de bajo costo. |
| Content Clone Agent | Available | Crea publicaciones, scripts de video corto y guiones de venta en vivo. |
| Sales Follow-up Agent | Available | Propone segmentación de clientes, mensajes de seguimiento y comunicación de precios. |
| Document Analyst Agent | Available | Lee PDF, Word, Excel y TXT para extraer resúmenes y listas de acción. |

## Features

- Available: flujo multi-agent, UI local con Streamlit, APIs OpenAI-compatible, carga de archivos, historial, exportación Markdown / DOCX.
- Experimental: modo de carpeta local para modelos GGUF.
- Planned: orquestación nativa con CrewAI, automatización del navegador, herramientas externas y permisos de equipo.

## Quick Start

```bash
git clone https://github.com/smclw/BossAgent.git
cd BossAgent
python -m venv .venv
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

## Security

No subas API keys, `.env`, datos privados de clientes ni archivos confidenciales. Las acciones externas deben requerir confirmación humana.

## License

MIT License.
