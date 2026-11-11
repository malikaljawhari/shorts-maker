# Practical Shorts production workflow

## Prepare before rendering

1. Choose a niche you can discuss responsibly with original insight: e.g., non-graphic gameplay mechanics, strategy tips, design comparisons or official gaming announcements.
2. Find topics with credible original sources. For news, verify the official release date and facts on the **day of publishing**.
3. Choose footage you recorded yourself or have permission and platform authorization to use. Save evidence in your private rights log.
4. Write a 20–45 second **original** script. A useful structure: first seconds = specific claim/question; next = evidence; last = explanation or conclusion. Don't present fan speculation as confirmed.
5. Record your voice (commercial rights clear) or choose a properly licensed AI narration service. For the current default edge-tts service, verify commercial permissions separately.

## In the Streamlit app

1. Select source video and an appropriate start/end range. The range applies to **video**, while the script or audio decides final run time.
2. Choose **Blurred background** to test first; when ready, try **Split-screen** with owned/authorized B-roll.
3. Paste a script and select voice mode. Own-voice mode accepts audio and optionally an aligned SRT. Without an SRT, word timing is only approximate.
4. Confirm you have rights and generate. Preview the entire video. Fix any subtitles or layout mistakes and regenerate.
5. Save the final file and private notes on the published topic, original source, permissions, and metadata.

## Publish and learn

Use YouTube Studio (preferably **Private** for the first review) and check publisher restrictions, audio, captions, crop, title accuracy and source links. Only then publish. Avoid volume for its own sake and avoid copying other people's posts. Be consistent enough to learn, without a guarantee of reaching the Shorts feed.

## 30-day experiment

| Time | Activity | What success actually means |
|---|---|---|
| Days 1–3 | Install, create synthetic demo, complete original private draft | A working local export you can explain |
| Days 4–7 | Publish a small number of reviewed, original clips | No copyright problems and a documented workflow |
| Week 2 | Try a few topics/durations/hooks | Comparable data for each Short |
| Week 3 | Analyze engaged views, retention and audience feedback | Evidence of which format is clearer/more interesting |
| Week 4 | Improve one feature in code, add tests, refine your content process | Portfolio-worthy technical contribution and an informed next step |

## Your tracking files

`analytics_template.csv` is a **blank example schema**, not actual results. Create `analytics.csv` locally and record publication date, topic, length, engaged views, retention and what you changed. Use `rights_log.csv` for permission evidence. Both are ignored by Git.

Use `PROMPTS.md` for scripts, fact-checking, transcript analysis and title brainstorming. Your own video-specific source research and final human decisions remain essential.
