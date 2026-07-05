# Security Policy

BossAgent is local-first, but users may upload sensitive documents and configure model API keys. Treat security as part of the product.

## Supported Versions

The project is currently in early MVP development. Security fixes should target the latest `main` branch.

## Reporting a Vulnerability

Please do not disclose vulnerabilities publicly before maintainers have a chance to review them. Use GitHub private vulnerability reporting when available, or open an issue with limited details and ask for a private channel.

## Safety Rules

- Never commit API keys, tokens, passwords, or `.env`.
- Never commit private customer data, uploaded documents, or local task databases.
- BossAgent must not execute code from uploaded files.
- Uploaded files should only be read for text extraction.
- Browser automation and external tools should be disabled by default.
- Sending, deleting, paying, ordering, or modifying external systems must require human confirmation.

## Local Data

Runtime data is stored under local folders such as `data/`, `uploads/`, `exports/`, and `models/`. These folders are ignored by Git except for `.gitkeep` placeholders.
