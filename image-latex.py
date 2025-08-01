import os
import re
import cv2
import easyocr
import numpy as np
import matplotlib.pyplot as plt
from sympy import sympify, latex, Eq
from PIL import Image

# config
INPUT_DIR  = os.path.join(os.getcwd(), 'input_')
OUTPUT_DIR = os.path.join(os.getcwd(), 'output')
OCR        = easyocr.Reader(['en'])

# process

def image_file_dir():
    et = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp') # extention to chexk the vaild img 
    return [
        os.path.join(INPUT_DIR, f)
        for f in os.listdir(INPUT_DIR)
        if f.lower().endswith(et)
    ]

def load_image(path):# open's image to load to process
    return Image.open(path)

def image_to_process(pil_img):# processes image
    arr  = np.array(pil_img.convert('RGB'))
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    mean_val = gray.mean()
    
    if mean_val > 127:
        # dark text on light bg is convertted to light text and dark  bg
        _, binary = cv2.threshold(
            gray, 0, 255,
            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )
    else:
        # light text on dark bg
        _, binary = cv2.threshold(
            gray, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
    return binary

def extract_text(binary_img):# we ectract text here
    """Run EasyOCR and collect all raw snippets."""
    return [txt for _, txt, _ in OCR.readtext(binary_img, detail=1)]

def clean_texts(raw_list):# extracted text are cleaned here
    """
    Preserve all math symbols, variables & punctuation.
    Adds explicit multiplication and strips junk.
    """
    cleaned = []
    for s in raw_list:
        t = (s
             .replace('×','*')
             .replace('−','-').replace('–','-')
             .replace('÷','/')
             .replace('X','x')
        )
        # this is to explicit multiplication: 2( to 2*(
        t = re.sub(r'(\d)\s*\(', r'\1*(', t)
        # here we strip control-chars but keep puntuation useful for math
        t = re.sub(r'[^\w\^\*\+\-=/\\\(\)\[\]\{\}\.,%:;<>|]', '', t)
        cleaned.append(t.strip())
    return cleaned

def to_latex(clean_list):# we convert the final text to latex for rendering
    out = []
    for txt in clean_list:
        try:
            if '=' in txt:
                lhs, rhs = txt.split('=', 1)
                eq = Eq(
                    sympify(lhs, evaluate=False),
                    sympify(rhs, evaluate=False),
                    evaluate=False
                )
                out.append(latex(eq))
            else:
                expr = sympify(txt, evaluate=False)
                out.append(latex(expr))
        except Exception as e:
            # fallback: render raw text if parsing fails
            out.append(txt)
        # continue processing next
    return out

def final_image(latex_snips, save_path,figsize=(8.27,11.7), fontsize=24, dpi=300): 
    # we render each image to a A4 size paper
    plt.figure(figsize=figsize)
    y = 0.9
    for code in latex_snips:
        # if it looks like raw text it will, render as it is
        if code and code[0] == '\\':
            txt = f"${code}$"
        else:
            txt = code
        plt.text(0.05, y, txt,
                 fontsize=fontsize, ha='left', va='center')
        y -= 0.08
        if y < 0.1:
            break  # if no space to fill characters
    plt.axis('off')
    plt.savefig(save_path,
                bbox_inches='tight', pad_inches=0, dpi=dpi)
    plt.close()

# main

if __name__ == '__main__':
    os.makedirs(INPUT_DIR,  exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i,path_in in enumerate(image_file_dir()):
        name, _   = os.path.splitext(os.path.basename(path_in))
        path_out  = os.path.join(OUTPUT_DIR, f"{name}{i}_latex.png")

        print(f"🔄 Processing: {path_in}")
        img       = load_image(path_in)
        binary    = image_to_process(img)
        raw       = extract_text(binary)
        cleaned   = clean_texts(raw)
        snippets  = to_latex(cleaned)
        final_image(snippets, path_out)
        print(f"  Saved → {path_out}")
