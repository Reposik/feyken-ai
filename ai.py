import os
import customtkinter as ctk
from groq import Groq
import threading

# Ключ подтянется из системы при сборке или из настроек GitHub
API_KEY = os.getenv("GROQ_API_KEY", "YOUR_KEY_HERE_FOR_TESTS")
CREATOR = "AzerOne / FEYKINS"

class FeykinCore:
    def __init__(self):
        self.client = Groq(api_key=API_KEY)
        self.model = "llama-3.3-70b-versatile"

    def generate_code(self, prompt):
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"Ты FEYKIN AI от {CREATOR}. Пиши только идеальный код."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Ошибка: {str(e)}"

class FeykinApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.ai = FeykinCore()
        self.title(f"FEYKIN AI - {CREATOR}")
        self.geometry("900x700")
        ctk.set_appearance_mode("dark")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkLabel(self, text="FEYKIN AI", font=("Consolas", 32, "bold"), text_color="#ff003c")
        self.header.grid(row=0, column=0, pady=20)

        self.code_display = ctk.CTkTextbox(self, font=("Consolas", 14))
        self.code_display.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.user_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Что кодим?", height=45)
        self.user_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.gen_button = ctk.CTkButton(self.input_frame, text="ПУСК", command=self.start_gen_thread, fg_color="#ff003c")
        self.gen_button.grid(row=0, column=1)

    def start_gen_thread(self):
        task = self.user_entry.get()
        if not task: return
        self.gen_button.configure(state="disabled", text="...")
        threading.Thread(target=self.run_ai, args=(task,), daemon=True).start()

    def run_ai(self, task):
        response = self.ai.generate_code(task)
        self.after(0, lambda: self.update_ui(response))

    def update_ui(self, response):
        self.code_display.insert("end", f"\n{response}\n")
        self.gen_button.configure(state="normal", text="ПУСК")

if __name__ == "__main__":
    app = FeykinApp()
    app.mainloop()
