import tkinter as tk
import threading
from game import run_game
from Form2 import open_ttc # ← імпортуємо TTC-вікно

root = tk.Tk()
root.title("Меню запуску гри")
root.geometry("450x350")
root.configure(bg="#1e1e1e")

label1 = tk.Label(root, text="432 група презентує ", font=("Arial", 16), fg="white", bg="#1e1e1e")
label1.pack(pady=10)

label2 = tk.Label(root, text="Ви можете бачити найкращий симулятор",
wraplength=400, justify="center", font=("Arial", 12), fg="white", bg="#1e1e1e")
label2.pack(pady=10)

# Кнопка запуску гри
button_start = tk.Button(root, text="Почати", font=("Arial", 12, "bold"), bg="green", fg="white",
                         command=lambda: threading.Thread(target=run_game).start())
button_start.place(x=30, y=120, width=100, height=40)

# Кнопка відкриття TTC
button_ttc = tk.Button(root, text="ТТХ", font=("Arial", 12, "bold"), bg="red", fg="white",
command=lambda: open_ttc(root))
button_ttc.place(x=300, y=120, width=100, height=40)

root.mainloop()
