# Publishing the project to GitHub (Windows)

## Before uploading

- Work inside the **new** project directory containing `app.py` and `README.md`.
- Never publish `token.json`, `client_secrets.json`, private keys, `.env`, videos from others, private analytics or permission messages. `.gitignore` excludes usual names, but **review `git status` manually**.
- Run tests and read the code. Rename/describe the project as your **AI-assisted, maintained project** rather than saying all code was written unaided.
- Optionally replace the neutral MIT copyright holder with a public author/organization name you are comfortable publishing; don't expose private personal details.

## Easiest option: GitHub Desktop

1. Install [GitHub Desktop](https://desktop.github.com/), sign into your GitHub account.
2. Unzip the new project. If the downloaded ZIP contains an outer folder, choose the **inner** folder with `README.md`.
3. In GitHub Desktop choose **File → Add Local Repository**; if it says the folder isn't a repository, select **create a repository here**.
4. Set repository name to `shorts-maker`, description to `Local Python/FFmpeg Shorts production app with captions and optional YouTube upload`.
5. Inspect changed files; check no `outputs/`, videos, credentials, or tokens are included. Make an initial commit.
6. Choose **Publish repository**. Consider **Private** while learning; you can change visibility to Public when ready.
7. Open the resulting repository URL, verify the README and Actions, and pin it to your GitHub profile if desired.

## Command line option

Install [Git for Windows](https://git-scm.com/downloads/win) and open PowerShell in the project root. Replace `YOUR_GITHUB_USERNAME` with your GitHub username.

```powershell
git --version
git init -b main
git status
git add .
git status
git commit -m "Initial release: Shorts Maker with tests and docs"
```

On GitHub choose **New repository**, name it `shorts-maker`, choose Private or Public. **Don't** select GitHub's initialize-with-README / .gitignore / license options: the local project already contains them. Then:

```powershell
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/shorts-maker.git
git push -u origin main
```

The browser/Git Credential Manager may ask you to authenticate. **Never paste your password/token into source code or chat.**

> If `git commit` says "Please tell me who you are", use `git config --global user.name "Your public display name"` and `git config --global user.email "your GitHub noreply email"` (find your **noreply** address in GitHub email settings). Use a privacy-safe public name.

## Confirm that GitHub is ready

- [ ] README renders and local setup instructions work on a fresh folder
- [ ] `.gitignore` hides `.venv`, outputs, API credentials and media
- [ ] License and AI-assistance disclosure remain accurate
- [ ] Code/tests/docs appear in the repository
- [ ] GitHub **Actions** Python tests start (may require enabling Actions)
- [ ] No private files appear under **Code** or any previous commit
- [ ] Screenshots, if uploaded, show only the app and not personal paths/names/media
- [ ] Repository description, 3–5 topics (`python`, `ffmpeg`, `streamlit`, `video-editing`, `automation`) and social preview are optional polish

## Updating after fixing a bug

```powershell
.\.venv\Scripts\python.exe -m pytest -q
git status
git add .
git commit -m "Fix subtitle timing validation"
git push
```

[GitHub's official instructions](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github)
