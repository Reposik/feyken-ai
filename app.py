import os
import customtkinter as ctk
from groq import Groq
import threading

# Гитхаб заменит слово PLACEHOLDER_KEY на твой реальный ключ при сборке
API_KEY = "PLACEHOLDER_KEY"

class FeykinApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FEYKIN AI - FIXED EDITION")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")

        self.output = ctk.CTkTextbox(self, width=760, height=450, font=("Consolas", 14))
        self.output.pack(padx=20, pady=20)

        self.entry_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.entry_frame.pack(padx=20, pady=10, fill="x")

        self.input = ctk.CTkEntry(self.entry_frame, placeholder_text="Теперь точно заработает. Пиши запрос...", height=40)
        self.input.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn = ctk.CTkButton(self.entry_frame, text="ПУСК", command=self.start, fg_color="#ff003c")
        self.btn.pack(side="right")

    def start(self):
        txt = self.input.get()
        if not txt: return
        self.btn.configure(state="disabled")
        threading.Thread(target=self.run, args=(txt,), daemon=True).start()

    def run(self, txt):
        try:
            # Если ключ всё еще заглушка, значит что-то пошло не так в Actions
            if API_KEY == "PLACEHOLDER_KEY":
                res = "Критическая ошибка: Ключ не был вшит при сборке!"
            else:
                client = Groq(api_key=API_KEY)
                chat = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": txt}]
                )
                res = chat.choices[0].message.content
        except Exception as e:
            res = f"ОШИБКА: {str(e)}"
        
        self.after(0, lambda: self.show(res))

    def show(self, res):
        self.output.delete("1.0", "end")
        self.output.insert("end", res)
        self.btn.configure(state="normal")

if __name__ == "__main__":
    app = FeykinApp()
    app.mainloop()
