# Security policy

This project is designed to run **locally**. It is not hardened for public Internet hosting.
Do not deploy the Streamlit interface to a public server without authentication, rate limits, resource limits, validation, and a security review.

- Never commit `client_secrets.json`, `token.json`, `.env`, user videos, or other people’s private media.
- OAuth runs locally. Do not paste access tokens or credentials into GitHub issues.
- YouTube URL mode is limited to HTTPS YouTube hosts. URLs should be used only with sufficient source-platform and copyright permissions.
- `subprocess` is invoked with argument arrays, not `shell=True`.
- Keep Python dependencies and FFmpeg updated, and inspect GitHub Dependabot/security alerts where available.

To report a security issue privately, use GitHub's private vulnerability reporting if enabled on the repository.
