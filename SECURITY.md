# Security Policy

Mind Your Skill is a public skill library. Skills may guide agents to use tools, edit files, call endpoints, or process private user data.

Security and privacy are core requirements.

## General policy

Skills must not:

- Hardcode private tokens or credentials
- Send user data to unknown endpoints
- Hide destructive behavior inside vague instructions
- Ask users to expose secrets publicly
- Delete or overwrite user data without clear intent

Skills should:

- Clearly disclose required permissions
- Use user-provided configuration for endpoints
- Prefer least-privilege access
- Ask for confirmation before destructive actions
- Keep setup and runtime behavior auditable

## Reporting issues

If you find a security issue, open a GitHub issue with a clear description.

Do not include private secrets, tokens, or sensitive user data in public reports.

## MoneyClip security notes

MoneyClip may interact with Google Sheets or a user-configured HTTP endpoint.

MoneyClip should only write to the sheet or endpoint configured by the user.

MoneyClip should not delete existing spreadsheet data during setup.

MoneyClip should not store hardcoded endpoint tokens in the repository.
