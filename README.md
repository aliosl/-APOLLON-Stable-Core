# 🎧 PROJECT APOLLON — Stable Core

**Apollon** is a minimalist YouTube audio player developed in **Python**, featuring a modern UI built with **CustomTkinter**.
It allows you to stream audio from YouTube videos or playlists using **yt-dlp** and **ffplay**.

> ⚠️ This project is an **experimental player** focused on UI and playback logic.
> It is **not** intended to be a full-featured media player like VLC.

> 🔒 **This project is strictly private and non-commercial.**
> It is developed for personal use only and must not be redistributed, sold, or used in any commercial context.

---

## ✨ Features

* 🎵 YouTube audio playback (single videos or playlists)
* 📜 Playlist display
* ⏮ / ⏭ Track navigation
* 🔀 Shuffle mode
* 🔁 Repeat mode
* ⏸ Pause / ▶ Resume *(restart-based — exact resume under maintenance)*
* 🎨 Modern UI (CustomTkinter)
* ⚡ Streaming only (no downloads)

---

## 🖥️ Technologies Used

* **Python 3.9+**
* **CustomTkinter**
* **yt-dlp**
* **ffplay** (FFmpeg)

---

## 📦 Requirements

### 1️⃣ Python

Python **3.9 or newer**

👉 [https://www.python.org/](https://www.python.org/)

---

### 2️⃣ FFmpeg (Required)

`ffplay` must be installed and available in your system `PATH`.

👉 [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

Verify installation:

```bash
ffplay -version
```

---

### 3️⃣ yt-dlp (Required)

`yt-dlp` is used to extract YouTube audio stream URLs.

Install via pip:

```bash
pip install yt-dlp
```

Verify installation:

```bash
yt-dlp --version
```

---

### 4️⃣ Python Dependencies

Install required Python libraries:

```bash
pip install customtkinter yt-dlp
```

---

## 🚀 Running the Project

```bash
python main.py
```

Paste a YouTube video or playlist URL into the input field and press **INVOKE DATA**.

---

## ⚠️ Notes & Limitations

* Audio playback relies on **ffplay**, not an internal audio engine
* Pause / Resume currently **restarts the track**
* No audio caching or offline playback
* YouTube access is handled via **yt-dlp (non-official extraction)**

---

## 🧠 Project Goal

Apollon is designed as a **learning and experimentation project**:

* UI architecture
* Player state management
* External process control
* Streaming logic

It is **not intended for commercial use**.

---

## 🔒 Private & Non-Commercial Use Only

This project is **strictly private**.

* ❌ Not for sale
* ❌ Not for redistribution
* ❌ Not for commercial use of any kind
* ✅ Personal use only

This project was created for personal learning and experimentation purposes.
Please respect YouTube's terms of service when using this software.

---

## 📜 License

This project is provided for **educational and personal purposes only**.
Use at your own risk and respect YouTube's terms of service.

---

## 🧩 Roadmap (Planned)

* ⏱ Exact pause / resume
* 🎚 Improved time tracking
* 🎧 Alternative audio backend
* 🧠 Cleaner state machine
* 🗂 Playlist caching

---

**PROJECT APOLLON — Stable Core**
Minimal. Focused. Experimental. Private.