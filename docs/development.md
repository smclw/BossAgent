# Development

## Project Structure

```text
BossAgent/
  app.py
  bossagent/
    agents.py
    config.py
    documents.py
    export.py
    llm.py
    orchestrator.py
    safety.py
    storage.py
  docs/
  data/
  uploads/
  exports/
  models/
```

## Add an Agent

1. Add a new `AgentSpec` in `bossagent/agents.py`.
2. Define role, goal, and output requirements.
3. Add it to `TASK_AGENT_MAP` in `bossagent/orchestrator.py`.
4. Add UI copy if the agent needs a new task type.
5. Test with mock mode and at least one real model provider when possible.

## Add a Tool

Keep tools isolated. Add a clear wrapper module and call it from the orchestrator or a specific agent. External write actions must require human confirmation.

## Modify the UI

The Streamlit UI lives in `app.py`.

Guidelines:

- Keep the app usable on a laptop screen.
- Avoid hiding critical controls behind decorative UI.
- Keep local-first behavior intact.
- Test Home, New Task, Upload, History, and Settings.

## Run Checks

```bash
python -m compileall app.py bossagent
```

Optional local smoke test:

```bash
streamlit run app.py
```

## Submit a PR

1. Fork the repository.
2. Create a feature branch.
3. Keep changes focused.
4. Update docs when behavior changes.
5. Confirm no private files are included.

## Avoid Private Data

Do not commit:

- `.env`.
- API keys.
- Uploaded files.
- SQLite databases.
- Generated reports.
- Local model files.
