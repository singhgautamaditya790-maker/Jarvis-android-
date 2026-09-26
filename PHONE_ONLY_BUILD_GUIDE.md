# JARVIS Cloud Build (phone-only instructions)

## Build APK using GitHub Actions from your Android phone

1. In Chrome, open https://github.com and create/sign in to a GitHub account.
2. Create a new repository. Name it `jarvis-android`. Choose Private if you prefer.
3. Upload these project files and folders to the repository root:
   - `main.py`
   - `buildozer.spec`
   - `.github/workflows/android.yml`
   IMPORTANT: GitHub must preserve the `.github/workflows/` folders.
4. Open the repository's Actions tab. If asked, enable Actions.
5. Select `Build JARVIS Android APK` in the left workflow list, then tap `Run workflow`.
   If you pushed files to `main`, the workflow may also start automatically.
6. Wait for the workflow to finish successfully. Open the completed run and scroll to Artifacts.
7. Download `JARVIS-debug-APK`, extract the downloaded artifact ZIP, then tap the APK to install.
8. If Android blocks installation, allow “Install unknown apps” for the browser/files app you used. Only install APKs from repositories/workflows you trust.

## Notes
- This is a debug APK for personal testing, not a Play Store release.
- GitHub Actions runs the build on cloud Linux; no PC is required. Builds can take a while on the first run.
- The source has a futuristic Kivy HUD UI, text input, time/date and web shortcuts. The microphone/Android speech and TTS integrations may need additional native Android bridging; do not assume all voice features are production-complete.
- Do not put OpenAI API keys in a public repository or inside an APK. Keys can be extracted. Use a private backend for real distribution.
