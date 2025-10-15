import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
from docx import Document

def open_ttc(parent):
    # Створюємо нове вікно
    ttc_window = tk.Toplevel(parent)
    ttc_window.title("TTC - Info")
    ttc_window.geometry("900x700")

    # --- Canvas + Scrollbars ---
    canvas = tk.Canvas(ttc_window)
    v_scrollbar = tk.Scrollbar(ttc_window, orient="vertical", command=canvas.yview)
    h_scrollbar = tk.Scrollbar(ttc_window, orient="horizontal", command=canvas.xview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    v_scrollbar.pack(side="right", fill="y")
    h_scrollbar.pack(side="bottom", fill="x")

    # -------- 1. Текст із Word --------
    doc = Document("assets/tactick.docx")
    text_content = "\n".join([p.text for p in doc.paragraphs if p.text.strip() != ""])

    label_text = tk.Label(scroll_frame, text=text_content, wraplength=850, justify="left")
    label_text.pack(pady=10)

    # -------- 2. Фото --------
    def add_image_pair(frame, img1, img2, caption):
        pair_frame = tk.Frame(frame)
        pair_frame.pack(pady=10)

        images = []
        for img_file in [img1, img2]:
            img = Image.open(img_file)
            img = img.resize((300, 200))
            photo = ImageTk.PhotoImage(img)
            images.append(photo)

        label1 = tk.Label(pair_frame, image=images[0])
        label1.image = images[0]
        label1.pack(side="left", padx=10)

        label2 = tk.Label(pair_frame, image=images[1])
        label2.image = images[1]
        label2.pack(side="left", padx=10)

        caption_label = tk.Label(frame, text=caption, font=("Arial", 12, "bold"))
        caption_label.pack()

    def add_image_single(frame, img_file, caption):
        img = Image.open(img_file)
        img = img.resize((350, 220))
        photo = ImageTk.PhotoImage(img)

        label = tk.Label(frame, image=photo)
        label.image = photo
        label.pack(pady=5)

        caption_label = tk.Label(frame, text=caption, font=("Arial", 12, "bold"))
        caption_label.pack()

    # --- Виводимо фото ---
    add_image_pair(scroll_frame, "assets/ATACMS.jpg", "assets/ATACMSS.jpg", "assets/Ракети ATACMS")
    add_image_single(scroll_frame, "assets/glsdb.jpg", "assets/Ракета GLSDB")
    add_image_single(scroll_frame, "assets/GMLRS.jpg", "assets/Ракета GMLRS")
    add_image_pair(scroll_frame, "assets/precision strike missile.jpg", "assets/PSM.jpg", "assets/Ракети Precision Strike")

    # -------- 3. Табличка з Excel --------
    df = pd.read_excel("assets/MisselsTTX.xlsx")

    frame_table = tk.Frame(scroll_frame)
    frame_table.pack(pady=10)

    tree = ttk.Treeview(frame_table, columns=list(df.columns), show="headings")

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

    # Додаємо скролбари для таблиці
    vsb = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame_table, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    frame_table.grid_rowconfigure(0, weight=1)
    frame_table.grid_columnconfigure(0, weight=1)
