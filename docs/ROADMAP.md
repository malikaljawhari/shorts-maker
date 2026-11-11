# Roadmap — ideas for personal contributions

## Good first engineering contributions

1. **Caption styles selector:** user chooses top/center/bottom and highlighted words; add unit/integration tests.
2. **Audio trim and fade:** avoid clipping the last syllable; include a few hundred milliseconds of tail.
3. **Saved project JSON:** save/load layout, timestamps, script and source filenames without bundling private videos.
4. **Rights log UI:** source URLs, permission category and notes, stored locally; never expose permissions publicly.
5. **Better error handling:** short useful errors for broken files and network timeouts.

## Further work (higher complexity)

- Locally transcribe **authorized** video and propose clip candidates, but require human review.
- Forced alignment for **your own** speech so captions match recorded words.
- A reproducible source library with rights/license metadata and reusable background footage.
- Batch **preview** generation; require approval before any upload.
- Optional analytics import and graphs, with no claims that metrics guarantee success.
- Signed Windows builds and user-friendly install/setup wizard after proper security review.

## Engineering issues to address before public hosting

The current web UI is designed for localhost. Public hosting requires account authentication, authorization, upload limits, anti-abuse controls, storage cleanup policies, quotas, server-side logging protection, and a legal review of video downloads and speech services. **Do not expose the current app to the public Internet as-is.**


### Natural voice improvements

- Add speech-aligned timestamps for Kokoro (currently estimated from text and total duration).
- Add optional voice comparison/export cache without storing private scripts outside the local computer.
- Allow short audio-only voice generation to save and re-use narration in multiple cuts.
- Investigate upstream Python 3.14 support; remove the sidecar only when stable upstream wheels exist.
