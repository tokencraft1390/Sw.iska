# Security Policy

## Supported status

Sw.iska is under active development. A deployment, payment flow, wallet integration, customer-data workflow, or autonomous action is not production-approved unless its release evidence explicitly says so.

## Reporting a vulnerability

Do not disclose suspected vulnerabilities, credentials, personal data, or exploit details in a public issue. Contact the repository owner through a previously verified private channel and include the affected commit, reproduction steps, impact, and proposed mitigation. Do not access other users' data, spend funds, or perform destructive testing.

## Security rules

- Never commit API keys, tokens, passwords, seed phrases, private keys, webhook secrets, customer records, or production configuration.
- Use separate development and production credentials with least privilege.
- External sending, publishing, deployment, spending, credential changes, data export, and wallet actions require explicit owner approval.
- Security checks and tests must pass before release.
- Rotate any credential suspected of exposure; deleting it from the latest commit is not sufficient.
- Preserve audit evidence, rollback instructions, and a tested recovery path.
- Third-party code, media, fonts, models, and data must have documented licenses and provenance.
- Protocol inputs must reject malformed, corrupted, replayed, or unknown events and must not create an implicit transaction-signing path.

