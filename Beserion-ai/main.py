import customtkinter as ctk
import threading
import datetime
from PIL import Image

# --- BACKEND BAĞLANTISI ---
try:
    from backend import BeserionBrain
    BACKEND_ACTIVE = True
except ImportError:
    BACKEND_ACTIVE = False

# --- TEMA AYARLARI ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue") # Temel tema (biz renkleri özelleştireceğiz)

# ÖZEL RENK PALETİ (BESERION THEME)
COLOR_BG = "#09090b"        # Simsiyah (Zinc 950)
COLOR_SIDE = "#18181b"      # Yan paneller (Zinc 900)
COLOR_USER = "#b91c1c"      # Kullanıcı Mesajı (Koyu Kırmızı - Red 700)
COLOR_BOT = "#27272a"       # Bot Mesajı (Koyu Gri - Zinc 800)
COLOR_ACCENT = "#dc2626"    # Vurgu Rengi (Parlak Kırmızı - Red 600)
TEXT_WHITE = "#fafafa"
TEXT_GREY = "#a1a1aa"

class BeserionApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere Ayarları
        self.title("Beserion-AI | Yahya Kracan Edition")
        self.geometry("500x750")
        self.minsize(400, 600)
        
        # Grid Sistemi
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) 

        # Beyni Başlat
        self.brain = BeserionBrain() if BACKEND_ACTIVE else None

        # --- 1. ÜST PANEL (HEADER) ---
        self.header = ctk.CTkFrame(self, fg_color=COLOR_SIDE, corner_radius=0, height=70)
        self.header.grid(row=0, column=0, sticky="ew")
        
        # Logo / Başlık
        self.lbl_title = ctk.CTkLabel(
            self.header, 
            text="BESERION", 
            font=("Impact", 24), # Sert bir font
            text_color=COLOR_ACCENT
        )
        self.lbl_title.pack(side="left", padx=20, pady=15)
        
        self.lbl_subtitle = ctk.CTkLabel(
            self.header, 
            text="v2.0", 
            font=("Arial", 12, "bold"), 
            text_color="white",
            fg_color="#3f3f46",
            corner_radius=5
        )
        self.lbl_subtitle.pack(side="left", pady=15)

        # Durum Işığı
        self.status_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        self.status_frame.pack(side="right", padx=20)
        
        self.lbl_status_dot = ctk.CTkLabel(self.status_frame, text="●", font=("Arial", 20), text_color="#22c55e")
        self.lbl_status_dot.pack(side="left")
        
        self.lbl_status_text = ctk.CTkLabel(self.status_frame, text="Aktif", font=("Arial", 12), text_color=TEXT_GREY)
        self.lbl_status_text.pack(side="left", padx=5)

        # --- 2. SOHBET ALANI ---
        self.chat_area = ctk.CTkScrollableFrame(
            self, 
            fg_color=COLOR_BG, 
            corner_radius=0
        )
        self.chat_area.grid(row=1, column=0, sticky="nsew")
        self.chat_area.grid_columnconfigure(0, weight=1)

        # --- 3. GİRİŞ ALANI (INPUT) ---
        self.input_frame = ctk.CTkFrame(self, fg_color=COLOR_SIDE, corner_radius=0, height=90)
        self.input_frame.grid(row=2, column=0, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        # Yazı Kutusu
        self.entry_msg = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Mevzuyu anlat...",
            height=50,
            corner_radius=10,
            border_width=1,
            border_color="#3f3f46",
            fg_color="#09090b",
            text_color="white",
            font=("Arial", 14)
        )
        self.entry_msg.grid(row=0, column=0, padx=15, pady=20, sticky="ew")
        self.entry_msg.bind("<Return>", self.send_event)

        # Gönder Butonu
        self.btn_send = ctk.CTkButton(
            self.input_frame,
            text="Yolla",
            width=80,
            height=50,
            corner_radius=10,
            fg_color=COLOR_ACCENT,
            hover_color="#b91c1c", # Tıklayınca koyulaşır
            text_color="white",
            font=("Arial", 14, "bold"),
            command=self.send_event
        )
        self.btn_send.grid(row=0, column=1, padx=(0, 15), pady=20)

        # Karşılama
        self.add_message("Ne var ne yok? Anlat bakalım derdini.", is_user=False)

    def send_event(self, event=None):
        msg = self.entry_msg.get()
        if not msg.strip(): return
        
        self.add_message(msg, is_user=True)
        self.entry_msg.delete(0, "end")
        self.entry_msg.configure(state="disabled") 
        
        # Durumu güncelle
        self.lbl_status_text.configure(text="Yazıyor...", text_color="#eab308")
        self.lbl_status_dot.configure(text_color="#eab308")

        threading.Thread(target=self.get_response_thread, args=(msg,), daemon=True).start()

    def get_response_thread(self, msg):
        try:
            if self.brain:
                response = self.brain.ask(msg)
            else:
                response = "Backend yok. Kafam çalışmıyor şu an."
        except Exception as e:
            response = f"Hata çıktı: {e}"

        self.after(0, self.post_response, response)

    def post_response(self, response):
        self.add_message(response, is_user=False)
        self.entry_msg.configure(state="normal")
        self.entry_msg.focus()
        
        self.lbl_status_text.configure(text="Aktif", text_color=TEXT_GREY)
        self.lbl_status_dot.configure(text_color="#22c55e")

    def add_message(self, text, is_user):
        """Mesaj Balonu Oluşturucu"""
        
        bubble_color = COLOR_USER if is_user else COLOR_BOT
        text_color = TEXT_WHITE
        avatar_text = "S" if is_user else "B"
        avatar_bg = COLOR_ACCENT if not is_user else "#3f3f46"
        
        # Ana Satır
        row_frame = ctk.CTkFrame(self.chat_area, fg_color="transparent")
        row_frame.pack(fill="x", pady=10, padx=10)

        # Avatar (Kare ama köşeleri hafif yuvarlak - Modern Stil)
        avatar = ctk.CTkLabel(
            row_frame,
            text=avatar_text,
            width=40, height=40,
            corner_radius=8,
            fg_color=avatar_bg,
            text_color="white",
            font=("Impact", 18)
        )

        # Mesaj Balonu
        bubble = ctk.CTkLabel(
            row_frame,
            text=text,
            fg_color=bubble_color,
            text_color=text_color,
            corner_radius=12,
            wraplength=320,
            font=("Arial", 14),
            padx=15, pady=12,
            justify="left"
        )

        # Zaman
        time_str = datetime.datetime.now().strftime("%H:%M")
        lbl_time = ctk.CTkLabel(row_frame, text=time_str, text_color="#52525b", font=("Arial", 10))

        # Hizalama
        if is_user:
            avatar.pack(side="right", anchor="n")
            bubble.pack(side="right", padx=10)
        else:
            avatar.pack(side="left", anchor="n")
            bubble.pack(side="left", padx=10)
        
        # Otomatik kaydır
        self.chat_area.update_idletasks()
        self.chat_area._parent_canvas.yview_moveto(1.0)

if __name__ == "__main__":
    app = BeserionApp()
    app.mainloop()