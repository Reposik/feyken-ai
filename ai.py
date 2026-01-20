import os
import customtkinter as ctk
from groq import Groq
import threading

# БЕЗОПАСНЫЙ ДОСТУП: ключ подтянется из GitHub Secrets при сборке
API_KEY = os.getenv("GROQ_API_KEY", "PASTE_KEY_HERE_FOR_LOCAL_TEST")
CREATOR = "AzerOne / FEYKINS"

class FeykinCore:
    def __init__(self):
        self.client = Groq(api_key=API_KEY)
        self.model = "llama-3.3-70b-versatile"

    def generate_code(self, prompt):
        system_msg = (
            f"Ты — FEYKIN AI, лучшая нейросеть для кодинга. Создатель: {CREATOR}. "
            "Пиши только идеальный, оптимизированный код. Используй SOLID и DRY. "
            "Отвечай технично и сразу к сути."
        )
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=4096
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Критическая ошибка (проверь API ключ): {str(e)}"

class FeykinApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.ai = FeykinCore()
        self.title(f"FEYKIN AI v1.0 - {CREATOR}")
        self.geometry("900x700")
        ctk.set_appearance_mode("dark")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkLabel(self, text="FEYKIN AI", font=("Consolas", 32, "bold"), text_color="#ff003c")
        self.header.grid(row=0, column=0, pady=20)

        self.code_display = ctk.CTkTextbox(self, font=("Consolas", 14), fg_color="#1a1a1a", border_color="#333", border_width=2)
        self.code_display.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.user_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Опиши задачу для идеального кода...", height=45)
        self.user_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.gen_button = ctk.CTkButton(self.input_frame, text="СГЕНЕРИРОВАТЬ", command=self.start_gen_thread, 
                                        fg_color="#ff003c", hover_color="#aa0028", height=45)
        self.gen_button.grid(row=0, column=1)

    def start_gen_thread(self):
        task = self.user_entry.get()
        if not task: return
        self.gen_button.configure(state="disabled", text="ДУМАЮ...")
        threading.Thread(target=self.run_ai, args=(task,), daemon=True).start()

    def run_ai(self, task):
        response = self.ai.generate_code(task)
        self.after(0, lambda: self.update_ui(response))

    def update_ui(self, response):
        self.code_display.insert("end", f"\n{response}\n" + "="*40 + "\n")
        self.code_display.see("end")
        self.gen_button.configure(state="normal", text="СГЕНЕРИРОВАТЬ")

if __name__ == "__main__":
    app = FeykinApp()
    app.mainloop()
