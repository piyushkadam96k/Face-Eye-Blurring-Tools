# 🎭 Face & Eye Blurring Tools 👁️

Welcome to the **Face & Eye Blurring** project! This repository contains two powerful Python scripts designed to protect privacy by blurring faces or eyes in videos and webcam feeds using **MediaPipe** and **OpenCV**.

---

## 📂 Files Description

### 1. `app.py` - 😶 Face Blur
This script detects faces in real-time and applies a Gaussian blur to the entire face region.
- **Technology**: MediaPipe Face Detection
- **Features**:
  - Works with **Webcam** or **Video Files**.
  - Fast and efficient face masking.

### 2. `eye.py` - 👁️ Eye Blur
This script specifically targets the eyes using facial landmarks and blurs them while keeping the rest of the face visible.
- **Technology**: MediaPipe Face Mesh
- **Features**:
  - Precise eye tracking (iris & surrounding area).
  - Ideal for partial anonymity.

---

## 🚀 How to Run

### 1️⃣ Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install opencv-python mediapipe
```

### 2️⃣ Run the Scripts
You can run either script using Python:

**For Face Blurring:**
```bash
python app.py
```

**For Eye Blurring:**
```bash
python eye.py
```

### 3️⃣ Choose Input Source
After running the script, follow the on-screen prompt:
- Type **`w`** for **Webcam**.
- Type **`v`** for **Video File** (then drag & drop the file).

---

## 🛑 Controls
- Press **`q`** to quit the application at any time.

---

✨ *Created with ❤️ by Amit Kadam* ✨
