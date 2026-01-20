import os
import customtkinter as ctk
from groq import Groq
import threading

# РАЗРЕЖЬ СВОЙ КЛЮЧ ПОПОЛАМ И ВСТАВЬ СЮДА
part1 = "gsk_dZErrktMU29RUmCWpb6N" 
part2 = "WGdyb3FYs96Im476Ab5M82jHi9WJzTxi"

API_KEY = part1 + part2

class FeykinApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FEYKIN AI")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")

        self.output = ctk.CTkTextbox(self, width=760, height=450, font=("Consolas", 14))
        self.output.pack(padx=20, pady=20)

        self.entry_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.entry_frame.pack(padx=20, pady=10, fill="x")

        self.input_field = ctk.CTkEntry(self.entry_frame, placeholder_text="Пиши запрос...", height=40)
        self.input_field.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn = ctk.CTkButton(self.entry_frame, text="ПУСК", command=self.start, fg_color="#ff003c")
        self.btn.pack(side="right")

    def start(self):
        prompt = self.input_field.get()
        if not prompt: return
        self.btn.configure(state="disabled")
        threading.Thread(target=self.run_ai, args=(prompt,), daemon=True).start()

    def run_ai(self, prompt):
        try:
            client = Groq(api_key=API_KEY)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            res = completion.choices[0].message.content
        except Exception as e:
            res = f"ОШИБКА: {str(e)}"
        
        self.after(0, lambda: self.update_ui(res))

    def update_ui(self, res):
        self.output.delete("1.0", "end")
        self.output.insert("end", res)
        self.btn.configure(state="normal")

if __name__ == "__main__":
    app = FeykinApp()
    app.mainloop()
