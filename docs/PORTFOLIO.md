# Portfolio, resume and LinkedIn wording

**Authorship:** Initial code was AI-assisted; be clear that you set it up, tested, modified and maintained it. Only claim features you personally tested or implemented. Do not say it has paying customers, earned revenue or is a production SaaS if that has not happened.

## Strong skills demonstrated by this codebase

**Tools/frameworks:** Python, Streamlit, FFmpeg, Git/GitHub, PowerShell, pytest, GitHub Actions, Google OAuth/YouTube Data API (optional).

**Software engineering concepts:** modular application design, asynchronous APIs, media processing, subprocess management, file handling, timestamps/validation, dependency management with virtual environments, unit/integration testing, error handling, automation and security-aware Git practices.

**Skills to claim carefully:** Python programming (if you can explain/modify the code), REST API integration (after testing the optional uploader), CI/CD (after GitHub Actions actually runs), frontend/UI design (basic Streamlit), technical documentation and troubleshooting.

**Do not claim yet:** machine learning model training, computer vision detection, automatic viral clip discovery, distributed/cloud systems, live SaaS deployment or automatic YouTube analytics integration. Those are not implemented.

## Resume draft — after finishing a real test export and reviewing the code

**Shorts Maker — Local AI-Assisted Video Automation Tool** | Python, Streamlit, FFmpeg, pytest, Git/GitHub

- Set up, customized and tested a local Streamlit application that converts authorized footage into vertical short-form videos with optional split-screen B-roll and caption overlays.
- Organized video-processing logic into a reusable Python module using FFmpeg for trimming, scaling, compositing and MP4 export.
- Added input validation, documentation and automated tests, including offline FFmpeg rendering tests in both supported layouts.
- Integrated optional speech generation and subtitle creation; built an alternative input path for personally recorded narration and SRT captions.

Use "developed" or "implemented" on a specific bullet only when you can honestly explain **your contribution** to it. Add measured results only after you record them.

## LinkedIn Projects section

**Project name:** Shorts Maker | Python Video Automation

**Associated with:** Personal project (leave company blank)

**Description:**

Created and customized an AI-assisted local video production tool using Python, Streamlit and FFmpeg. The application trims authorized footage, combines optional background video, adds narration and captions, and exports vertical MP4 files. I configured the Windows development environment, documented the architecture, tested media-processing functionality and am improving the application through additional features and validation.

**Skills:** Python, FFmpeg, Streamlit, Git, GitHub, Software Testing, Automation, API Integration (only after testing the uploader)

**Project URL:** `https://github.com/YOUR_GITHUB_USERNAME/shorts-maker` (replace only after repo exists)

## LinkedIn update post (optional; after publishing and testing)

I’ve been working on a personal software project called **Shorts Maker**, a local Python application for creating narrated vertical videos from authorized footage.

It uses **Streamlit** for the interface and **FFmpeg** for trimming, resizing, split-screen layouts, captions and MP4 export. I also worked through Python environment setup, troubleshooting and automated tests. The initial prototype was AI-assisted, and I’m using it as a practical way to learn software engineering by studying, customizing and extending the code.

Next, I plan to improve caption synchronization and add better project management for clips.

Code and documentation: [REPOSITORY LINK]

## LinkedIn eligibility

LinkedIn requires members to be **at least 16**, or older where local rules require a higher minimum age. If you aren't eligible yet, save this draft for later; don't bypass account age requirements. See https://www.linkedin.com/help/linkedin/answer/a6854067.

## Interview discussion prompts

Be prepared to explain (a) why `subprocess.run` is used with argument arrays, (b) the difference between video length and narration length, (c) why ffprobe is used to validate source duration, (d) why source downloads and OAuth tokens have permissions/privacy risks, (e) how you tested the renderer without using other people's videos, and (f) which code you personally changed.
