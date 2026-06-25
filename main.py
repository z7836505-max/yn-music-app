import tkinter as tk
from tkinter import ttk
import asyncio
import edge_tts
import threading

class MFMTTSApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MFMTTS - AI Voice Premium")
        self.root.geometry("500x520")
        self.root.resizable(False, False)
        
        # --- DARK THEME STYLE ---
        self.BG_COLOR = "#1e1e2e"       # Dark Background
        self.CARD_COLOR = "#252538"     # Input Box Background
        self.TEXT_COLOR = "#cdd6f4"     # Light Text
        self.ACCENT_COLOR = "#89b4fa"   # Blue Accent
        
        self.root.configure(bg=self.BG_COLOR)
        
        # Style Configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", background=self.BG_COLOR, foreground=self.TEXT_COLOR)
        self.style.configure("TLabel", background=self.BG_COLOR, foreground=self.TEXT_COLOR)
        
        # Title
        label_title = tk.Label(self.root, text="MFMTTS AI Voice Generator", font=("Segoe UI", 18, "bold"), fg=self.ACCENT_COLOR, bg=self.BG_COLOR)
        label_title.pack(pady=20)

        # Label Text
        label_text = ttk.Label(self.root, text="အသံပြောင်းလိုသော မြန်မာစာသားများကို ဒီမှာရိုက်ထည့်ပါ -", font=("Segoe UI", 11))
        label_text.pack(pady=5)

        # Text Box (Modern Dark Style)
        self.textbox = tk.Text(self.root, width=48, height=8, font=("Segoe UI", 12), bg=self.CARD_COLOR, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR, relief="flat", bd=0, padx=10, pady=10)
        self.textbox.pack(pady=5)
        self.textbox.insert("1.0", "မင်္ဂလာပါခင်ဗျာ။ ဒီနေ့မှာတော့ ပရိသတ်တွေအကြိုက်တွေ့စေမယ့် ရုပ်ရှင်ဇာတ်လမ်းကောင်းတစ်ခုကို တင်ဆက်ပေးသွားမှာဖြစ်ပါတယ်။")

        # Voice Select
        label_voice = ttk.Label(self.root, text="AI အသံရွေးချယ်ရန် -", font=("Segoe UI", 11))
        label_voice.pack(pady=10)
        
        self.voice_var = tk.StringVar()
        self.voice_option = ttk.Combobox(self.root, textvariable=self.voice_var, state="readonly", width=28)
        self.voice_option['values'] = ("အမျိုးသမီးသံ (Nilar)", "အမျိုးသားသံ (Thiha)")
        self.voice_option.current(0)
        self.voice_option.pack(pady=5)

        # Button (Modern Styled Button)
        self.btn_generate = tk.Button(self.root, text="အသံဖိုင်အဖြစ် ပြောင်းမည်", command=self.start_generation, font=("Segoe UI", 11, "bold"), bg="#45475a", fg=self.ACCENT_COLOR, activebackground=self.ACCENT_COLOR, activeforeground=self.BG_COLOR, relief="flat", width=22, height=1, bd=0, cursor="hand2")
        self.btn_generate.pack(pady=25)

        # Status
        self.label_status = tk.Label(self.root, text="အခြေအနေ: အဆင်သင့်", font=("Segoe UI", 11), fg="#a6e3a1", bg=self.BG_COLOR)
        self.label_status.pack(pady=5)

    def start_generation(self):
        threading.Thread(target=self.run_tts, daemon=True).start()

    def run_tts(self):
        text = self.textbox.get("1.0", "end").strip()
        if not text:
            self.label_status.configure(text="အခြေအနေ: ကျေးဇူးပြု၍ စာသားထည့်ပေးပါ!", fg="#f38ba8")
            return

        self.label_status.configure(text="အသံဖိုင်ပြောင်းနေပါပြီ... ခေတ္တစောင့်ပါ...", fg="#fab387")
        self.btn_generate.configure(state="disabled", bg="#313244")

        voice_choice = self.voice_var.get()
        voice = "my-MM-NilarNeural" if "Nilar" in voice_choice else "my-MM-ThihaNeural"

        async def save_audio():
            communicate = edge_tts.Communicate(text, voice, rate="+10%")
            await communicate.save("my_ai_voice.mp3")

        try:
            asyncio.run(save_audio())
            self.label_status.configure(text="အောင်မြင်စွာ ပြောင်းလဲပြီးပါပြီ! (my_ai_voice.mp3)", fg="#a6e3a1")
        except Exception as e:
            self.label_status.configure(text=f"Error: {str(e)}", fg="#f38ba8")
        
        self.btn_generate.configure(state="normal", bg="#45475a")

if __name__ == "__main__":
    app = MFMTTSApp()
    app.root.mainloop()