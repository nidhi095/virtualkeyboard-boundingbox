# 🖐️ Virtual Keyboard with Bounding Box Interaction

This project is a **virtual keyboard** that lets users type by moving their **index finger** over on-screen keys. It uses **computer vision** to detect finger positions in real-time and simulates keypresses when the finger enters a bounding box representing a key.

---

## 🚀 Features

- Real-time finger tracking using OpenCV and MediaPipe  
- On-screen virtual keyboard with bounding boxes  
- Keypress detection when finger enters a key region  
- Customizable keyboard layout and key size  
- Visual feedback for pressed keys  

---

## 🧠 How It Works

1. Captures frames from your webcam.  
2. Detects hand landmarks (especially the index finger tip).  
3. Checks if the finger tip lies within any key’s bounding box.  
4. If true, triggers a key press and highlights that key.  

---
## 🛠️ Future Improvements

-Add debounce logic to prevent multiple detections
-Improve key layout customization
-Add sound or text output
-Implement gesture-based control
