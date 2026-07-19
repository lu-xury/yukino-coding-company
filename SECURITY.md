# Security policy

## Supported version

Only the latest commit on the default branch is supported.

## Reporting a vulnerability

Do not publish security-sensitive details in a public issue. Use GitHub's
private vulnerability reporting when enabled, or contact the repository owner
through their GitHub profile.

This project contains static images, JSON, Markdown, a local Python validator,
and GitHub workflow configuration. Reports are especially useful for:

- unsafe installation instructions;
- path traversal or unintended file writes in validation tooling;
- dependency or workflow supply-chain risks;
- malformed files that cause excessive resource use;
- instructions that overwrite unrelated Codex pets.

Please include reproduction steps, impact, affected commit, and a suggested
fix when possible.
