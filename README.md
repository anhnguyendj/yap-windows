# Yap for Windows 🎙️

> Push-to-talk dictation app for Windows — hold Space, speak, text auto-pastes anywhere.

Inspired by [haynoi](https://github.com/sonpiaz/haynoi) (macOS). This is the Windows version built with Python.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Windows](https://img.shields.io/badge/Windows-10%2F11-blue) ![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

- **Hold Space** → speak → text auto-pastes into any active window
- Vietnamese + English support (Whisper multilingual)
- Groq Whisper Large v3 Turbo — free, 2000 min/day
- Beautiful dark UI with animated mic canvas
- Lives in system tray, always ready
- History panel with click-to-copy

## Demo

Hold Space → speak → release → text appears where your cursor is.

---

## Setup

**1. Clone the repo**
```
git clone https://github.com/anhnguyendj/yap-windows.git
cd yap-windows
```

**2. Run setup** (installs all dependencies)
```
setup.bat
```

**3. Add your Groq API key**
- Get a free key at [console.groq.com](https://console.groq.com)
- Open the app → click ⚙ Settings → paste your key → Save & Apply

**4. Run**
```
run.bat
```

Or create a desktop shortcut:
```
python make_shortcut.py
```

---

## Requirements

- Windows 10/11 (64-bit)
- Python 3.10+
- Microphone
- Free [Groq API key](https://console.groq.com) (or OpenAI)

Dependencies (auto-installed by `setup.bat`):
```
sounddevice numpy keyboard pyperclip groq Pillow pystray pywin32 customtkinter
```

---

## Usage

| Action | Result |
|--------|--------|
| Hold **Space** (>0.4s) | Start recording |
| Release **Space** | Stop & transcribe |
| Quick tap **Space** | Normal space character |
| Click tray icon | Show/hide window |

### Settings
- **Provider**: Groq (free) or OpenAI
- **Language**: Vietnamese / English / Auto-detect
- **Hold key**: Change from Space to any key (Ctrl, F9, etc.)

---

## Project Structure

```
yap-windows/
├── app.py              # Main application
├── make_shortcut.py    # Creates desktop shortcut + icon
├── setup.bat           # Install dependencies
├── run.bat             # Launch app
└── requirements.txt    # Python packages
```

---

## How it works

1. `GetAsyncKeyState` polls the hotkey at 5ms intervals
2. Hold detected → `sounddevice` records audio at 16kHz
3. Audio sent to Groq Whisper Large v3 Turbo via API
4. Transcribed text copied to clipboard → `Ctrl+V` auto-pasted

---

## Credits

- Inspired by [haynoi](https://github.com/sonpiaz/haynoi) by [@sonpiaz](https://github.com/sonpiaz)
- Powered by [Groq](https://groq.com) + [OpenAI Whisper](https://openai.com/research/whisper)

---

## License

MIT
