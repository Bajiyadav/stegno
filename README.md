

readme_content = '''
# XOR Steganography GUI 🔐🖼️

This Python project enables users to **hide (encode)** and **reveal (decode)** secret messages inside images using a combination of **XOR encryption** and **Least Significant Bit (LSB) steganography**, all through a simple **Tkinter GUI**.

---

## 🧠 Features

- XOR encryption using a numeric key
- GUI-based image selection and message entry
- Encodes messages into image pixels (LSB)
- Saves encrypted message and binary to files
- Decodes hidden messages with the correct key
- Shows progress using `tqdm`
- Works with `.png` and `.jpg` images

---

## 🛠 Technologies Used

- Python 3
- OpenCV (`cv2`)
- NumPy
- Pillow (PIL)
- Tkinter
- tqdm

---

## 💻 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/Bajiyadav/xor-steganography-gui2.git
cd xor-steganography-gui2
