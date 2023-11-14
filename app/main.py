from .gui.main_window import App
import customtkinter as ctk

def run_app():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()
