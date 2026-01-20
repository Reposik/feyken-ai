import os
import customtkinter as ctk
from groq import Groq
import threading
import sys

# Берем ключ из секретов GitHub (при сборке) или из системы
API_KEY = os.environ.get("GROQ_API_KEY", "")

class FeykinAI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("FEYKIN AI PRO - AZER EDITION")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")
        
        # Заголовок
        self.label = ctk.CTkLabel(self, text="FEYKIN AI", font=("Arial", 24, "bold"), text_color="#ff003c")
        self.label.pack(pady=10)

        # Поле вывода
        self.result_text = ctk.CTkTextbox(self, width=760, height=400, font=("Consolas", 14))
        self.result_text.pack(padx=20, pady=10)

        # Поле ввода
        self.input_field = ctk.CTkEntry(self, placeholder_text="Введите ваш запрос...", width=600, height=40)
        self.input_field.pack(side="left", padx=(20, 10), pady=20)

        # Кнопка
        self.btn = ctk.CTkButton(self, text="ПУСК", command=self.send_request, fg_color="#ff003c", hover_color="#b3002a")
        self.btn.pack(side="right", padx=(0, 20), pady=20)

    def send_request(self):
        prompt = self.input_field.get()
        if not prompt: return
        
        if not API_KEY:
            self.result_text.insert("end", "\n[!] Ошибка: Ключ API не найден. Проверь GitHub Secrets!\n")
            return

        self.btn.configure(state="disabled")
        threading.Thread(target=self.call_groq, args=(prompt,), daemon=True).start()

    def call_groq(self, prompt):
        try:
            client = Groq(api_key=API_KEY)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            response = completion.choices[0].message.content
            self.after(0, lambda: self.show_response(response))
        except Exception as e:
            self.after(0, lambda: self.show_response(f"Ошибка: {str(e)}"))

    def show_response(self, text):
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", text)
        self.btn.configure(state="normal")

if __name__ == "__main__":
    app = FeykinAI()
    app.mainloop()
