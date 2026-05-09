import os
import subprocess
import threading
import random
import customtkinter as ctk
import yt_dlp
import time

# --- STYLE P3R ---
P3_THEME = {"CYAN": "#00d4ff", "DEEP": "#050b14", "CARD": "#0a1a2e", "ACCENT": "#1a2e45", "TEXT": "#7a8da1"}

class ApollonFinalEngine(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PROJECT APOLLON // STABLE CORE")
        self.geometry("1100x650")
        self.configure(fg_color=P3_THEME["DEEP"])

        # Logique
        self.process = None
        self.playlist_data = [] 
        self.current_idx = 0
        self.is_loading = False 
        self.is_paused = False # NOUVEL ÉTAT PAUSE
        
        # Modes
        self.is_shuffle = False
        self.is_repeat = False

        self.setup_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        self.player_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.player_frame.pack(side="left", fill="both", expand=True, padx=20)

        self.header = ctk.CTkLabel(self.player_frame, text="ATHENA SYSTEM", font=("Impact", 36), text_color=P3_THEME["CYAN"])
        self.header.pack(pady=30)

        self.url_input = ctk.CTkEntry(self.player_frame, placeholder_text="PASTE YOUTUBE URL...", width=450, height=45, fg_color=P3_THEME["CARD"])
        self.url_input.pack()

        self.btn_load = ctk.CTkButton(self.player_frame, text="INVOKE DATA", command=self.start_sync, 
                                      fg_color=P3_THEME["CYAN"], text_color=P3_THEME["DEEP"], font=("Impact", 18))
        self.btn_load.pack(pady=15)

        self.status_card = ctk.CTkFrame(self.player_frame, width=450, height=120, fg_color=P3_THEME["CARD"], corner_radius=15)
        self.status_card.pack(pady=10)
        self.status_card.pack_propagate(False)

        self.status = ctk.CTkLabel(self.status_card, text="SYSTEM READY", font=("Consolas", 14), text_color=P3_THEME["TEXT"], wraplength=400)
        self.status.pack(expand=True)
        
        self.time_container = ctk.CTkFrame(self.player_frame, fg_color="transparent")
        self.time_container.pack(fill="x", padx=50, pady=10)

        self.time_label = ctk.CTkLabel(self.time_container, text="00:00 / 00:00", font=("Consolas", 16, "bold"), text_color=P3_THEME["CYAN"])
        self.time_label.pack()

        self.progress_bar = ctk.CTkProgressBar(self.player_frame, width=450, height=8, fg_color=P3_THEME["ACCENT"], progress_color=P3_THEME["CYAN"])
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=5)

        # Contrôles de lecture
        self.ctrls = ctk.CTkFrame(self.player_frame, fg_color="transparent")
        self.ctrls.pack(pady=20)
        
        ctk.CTkButton(self.ctrls, text="⏮", width=70, height=45, font=("Arial", 20), command=self.prev_track).grid(row=0, column=0, padx=5)
        
        # BOUTON HALT (DEVIENT PLAY/PAUSE)
        self.btn_halt = ctk.CTkButton(self.ctrls, text="HALT", width=100, height=45, fg_color="#ff4b4b", font=("Impact", 16), command=self.toggle_pause)
        self.btn_halt.grid(row=0, column=1, padx=5)
        
        ctk.CTkButton(self.ctrls, text="⏭", width=70, height=45, font=("Arial", 20), command=self.skip_track).grid(row=0, column=2, padx=5)

        self.modes = ctk.CTkFrame(self.player_frame, fg_color="transparent")
        self.modes.pack()
        
        self.btn_shuff = ctk.CTkButton(self.modes, text="SHUFFLE: OFF", width=120, fg_color=P3_THEME["ACCENT"], command=self.toggle_shuffle)
        self.btn_shuff.grid(row=0, column=0, padx=5)
        
        self.btn_rep = ctk.CTkButton(self.modes, text="REPEAT: OFF", width=120, fg_color=P3_THEME["ACCENT"], command=self.toggle_repeat)
        self.btn_rep.grid(row=0, column=1, padx=5)

        self.list_frame = ctk.CTkFrame(self, width=380, fg_color=P3_THEME["CARD"], corner_radius=0)
        self.list_frame.pack(side="right", fill="both")
        self.scroll = ctk.CTkScrollableFrame(self.list_frame, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=5, pady=5) 
        
    def toggle_pause(self):
        if not self.process or self.is_loading:
            return

        if not self.is_paused:
            # PAUSE = arrêt du process
            self.is_paused = True
            self.btn_halt.configure(text="RESUME", fg_color=P3_THEME["CYAN"], text_color=P3_THEME["DEEP"])
            self.status.configure(text="SYSTEM PAUSED")
            self.stop_all()


    def stop_all(self):
        """Arrêt total (utilisé pour changer de morceau ou fermer)"""
        if self.process:
            try:
                self.process.stdin.write(b'q') # 'q' pour quitter ffplay proprement
                self.process.stdin.flush()
                self.process.terminate()
            except: pass
        os.system("taskkill /f /im ffplay.exe >nul 2>&1")
        self.process = None
        self.is_paused = False
        self.btn_halt.configure(text="HALT", fg_color="#ff4b4b", text_color="white")

    def start_sync(self):
        url = self.url_input.get()
        if not url or self.is_loading: return
        self.status.configure(text="DECODING DATA...")
        self.stop_all()
        threading.Thread(target=self.extract_data, args=(url,), daemon=True).start()

    def extract_data(self, url):
        self.is_loading = True
        ydl_opts = {'extract_flat': True, 'quiet': True, 'no_warnings': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    self.playlist_data = [{'title': e.get('title', 'Unknown '), 'url': e['url']} for e in info['entries']]
                else:
                    self.playlist_data = [{'title': info.get('title', 'Unknown '), 'url': url}]
            
            self.current_idx = 0
            self.after(0, self.update_list_ui)
            self.play_node()
        except:
            self.after(0, lambda: self.status.configure(text="ERROR: UNREACHABLE"))
        finally:
            self.is_loading = False

    def play_node(self):
        if not self.playlist_data or self.is_loading: return
        self.stop_all()
        node = self.playlist_data[self.current_idx]
        self.after(0, self.update_list_ui)
        self.after(0, lambda: self.status.configure(text=f"INVOKING: {node['title'][:50]}"))
        threading.Thread(target=self._execute_stream, args=(node['url'],), daemon=True).start()

    def _execute_stream(self, url):
        self.is_loading = True
        try:
            with yt_dlp.YoutubeDL({'format': 'bestaudio', 'quiet': True, 'no_warnings': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                stream_url = info['url']

            # IMPORTANT: Ajout de stdin=subprocess.PIPE pour pouvoir envoyer 'p' (pause) ou 'q' (quitter)
            cmd = ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', '-vn', stream_url]
            self.process = subprocess.Popen(cmd, stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
            
            self.is_loading = False
            self.process.wait()
            
            # Si le processus s'arrête de lui-même (fin du morceau) et qu'on n'est pas en pause
            if self.process is not None and not self.is_paused:
                if self.is_repeat:
                    self.after(0, self.play_node)
                else:
                    self.after(0, self.skip_track)
        except:
            self.is_loading = False

    def skip_track(self):
        if not self.playlist_data or self.is_loading: return
        self.current_idx = (self.current_idx + 1) % len(self.playlist_data)
        self.play_node()

    def prev_track(self):
        if not self.playlist_data or self.is_loading: return
        self.current_idx = (self.current_idx - 1) % len(self.playlist_data)
        self.play_node()

    def jump_to(self, index):
        self.current_idx = index
        self.play_node()

    def on_closing(self):
        self.stop_all()
        self.destroy()
        os._exit(0)

    def toggle_shuffle(self):
        self.is_shuffle = not self.is_shuffle
        self.btn_shuff.configure(text=f"SHUFFLE: {'ON' if self.is_shuffle else 'OFF'}", 
                                 fg_color=P3_THEME["CYAN"] if self.is_shuffle else P3_THEME["ACCENT"])

    def toggle_repeat(self):
        self.is_repeat = not self.is_repeat
        self.btn_rep.configure(text=f"REPEAT: {'ON' if self.is_repeat else 'OFF'}", 
                               fg_color=P3_THEME["CYAN"] if self.is_repeat else P3_THEME["ACCENT"])

    def update_list_ui(self):
        for w in self.scroll.winfo_children(): w.destroy()
        for i, item in enumerate(self.playlist_data):
            is_active = (i == self.current_idx)
            btn = ctk.CTkButton(self.scroll, text=f"{'▶ ' if is_active else ''}{item['title'][:45]}", 
                                anchor="w", fg_color=P3_THEME["ACCENT"] if is_active else "transparent",
                                text_color=P3_THEME["CYAN"] if is_active else "white",
                                command=lambda idx=i: self.jump_to(idx))
            btn.pack(fill="x", pady=2)

if __name__ == "__main__":
    app = ApollonFinalEngine()
    app.mainloop()