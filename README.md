# Image-to-LaTeX Converter

This Python tool extracts mathematical equations and text from images using **EasyOCR**, processes them with **SymPy**, and converts them into LaTeX-rendered images.

---

## 📌 Features
- Supports **dark-on-light** and **light-on-dark** text detection.
- Automatically extracts and cleans text, preserving math symbols and variables.
- Converts equations into LaTeX for accurate mathematical rendering.
- Renders output on an **A4-sized image** for easy use in reports or documents.

---

## 🛠️ Tools & Libraries Used
- **Python 3.x**
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) – Optical character recognition
- [OpenCV](https://opencv.org/) – Image preprocessing (grayscale & thresholding)
- [SymPy](https://www.sympy.org/) – Math parsing and LaTeX conversion
- [Matplotlib](https://matplotlib.org/) – Rendering output images
- [Pillow (PIL)](https://python-pillow.org/) – Image handling
- `os`, `re`, `numpy` for utilities

---

## 🔧 Installation

Clone the repository:
```bash
git clone https://github.com/<your-username>/image-latex.git
cd image-latex

Install dependencies:
pip install easyocr opencv-python numpy sympy matplotlib pillow

▶️ Usage
Place your input images (equations/screenshots) in the input_ folder.
Run the script:
python image-latex.py
Processed LaTeX-rendered outputs will be saved in the output folder.

📂 Project Structure
bash
Copy
Edit
image-latex/
│── input_/       # Folder for input images
│── output/       # Generated LaTeX-rendered images
│── image-latex.py
│── README.md

🖼️ Sample Output
Input Image:

Output Rendered:

🎯 Objective
This tool simplifies the conversion of math problems (from images or handwritten notes) into neat LaTeX-rendered outputs, useful for documentation, assignments, or research.

✍️ Author
Yuvraj (Vruk)
Programming Enthusiast | Python Developer
GitHub
