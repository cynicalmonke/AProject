import tkinter as tk
import customtkinter as ctk
from ..data.database import Database

# Creating the Page base class
class Page(ctk.CTk):
    def __init__(self, parent=None, color="#9dcef2"):     
        super().__init__()
        self.configure(bg=color)  # Set the background color here
        self.parent = parent

    def show_sidebar(self):
        """Display the common sidebar for all pages except settings."""
        for widget in self.parent.sidebar_frame.winfo_children():
            widget.destroy()

        self.parent.logo_label = ctk.CTkLabel(self.parent.sidebar_frame, text="AProject", font=ctk.CTkFont(size=20, weight="bold"), padx=10)
        self.parent.logo_label.pack(padx=(23, 10), pady=(12, 14), anchor="w")

        self.sidebar_button_1 = ctk.CTkButton(
            self.parent.sidebar_frame,
            text="+ Collection  ",
            corner_radius=0,
            anchor="center",
            font=ctk.CTkFont(size=17), 
            height=50,
            command=self.add_new_button
        )
        self.sidebar_button_1.pack(fill="x", pady=2)

        # Create Scrollable frame for collections here
        self.scrollable_frame = ctk.CTkScrollableFrame(self.sidebar_frame)
        self.scrollable_frame.pack(fill="both", expand=True)

        # Intermediate frame inside the scrollable frame
        self.inner_frame = tk.Frame(self.scrollable_frame, bg='#9dcef2')
        self.inner_frame.pack(fill="both", expand=True)

        # Populate the inner frame with the saved collections from the database
        self.populate_collections_from_db()


# Creating subclasses for each page
class CollectionsPage(Page):
    def __init__(self, parent=None, color="#9dcef2"):
        super().__init__(parent)
        self.configure(bg=color)
        # Add widgets for the collections page here
        self.parent.show_sidebar()
        # Create a canvas for the masonry layout
        self.canvas = tk.Canvas(self, bg='#9dcef2')
        self.canvas.grid(row=1, column=1, sticky="nsew")

        # Add a scrollbar to the canvas
        self.scrollbar = ctk.CTkScrollbar(self.canvas)
        self.scrollbar.grid(row=1, column=2, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold the widgets
        self.masonry_frame = tk.Frame(self.canvas, bg='#9dcef2')
        self.canvas.create_window((0, 0), window=self.masonry_frame, anchor="nw")

        self.masonry_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Bind the mouse wheel event to the masonry_frame and the canvas
        self.masonry_frame.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Configure>", self.adjust_masonry_layout)

        # Sample widgets for the masonry layout
        self.widgets = []
        for i in range(20):
            frame = tk.Frame(self.masonry_frame, width=200, height=150, bg=f"#{i*5%256:02x}{i*10%256:02x}{i*15%256:02x}")
            frame.pack(padx=10, pady=10)
            frame.bind("<MouseWheel>", self.on_mousewheel)
            self.widgets.append(frame)



class ImportPage(Page):
    def __init__(self, parent):
        super().__init__(parent)
        # Add widgets for the import page here
        self.parent.show_sidebar()
        # Create a canvas for the masonry layout
        self.canvas = tk.Canvas(self, bg="#9dcef2")
        self.canvas.grid(row=1, column=1, sticky="nsew")

        # Add a scrollbar to the canvas
        self.scrollbar = ctk.CTkScrollbar(self.canvas)
        self.scrollbar.grid(row=1, column=2, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold the widgets
        self.masonry_frame = tk.Frame(self.canvas, bg="#9dcef2")
        self.canvas.create_window((0, 0), window=self.masonry_frame, anchor="nw")

        self.masonry_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Bind the mouse wheel event to the masonry_frame and the canvas
        self.masonry_frame.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Configure>", self.adjust_masonry_layout)

        # Sample widgets for the masonry layout
        self.widgets = []
        for i in range(20):
            frame = tk.Frame(self.masonry_frame, width=200, height=150, bg=f"#{i*5%256:02x}{i*10%256:02x}{i*15%256:02x}")
            frame.pack(padx=10, pady=10)
            frame.bind("<MouseWheel>", self.on_mousewheel)
            self.widgets.append(frame)



class UsbPage(Page):
    def __init__(self, parent):
        super().__init__(parent)
        # Add widgets for the usb page here
        self.parent.show_sidebar()



class SettingsPage(Page):
    def __init__(self, parent):
        super().__init__(parent)
        # Add widgets for the settings page here
        self.parent.show_sidebar()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#9dcef2")
        self.db = Database()
        self.configure_app()
        self.create_sidebar_frame()
        self.create_navbar()

        # Storing the pages in a dictionary
        self.pages = {}
        for PageClass in (CollectionsPage, ImportPage, UsbPage, SettingsPage):
            page_instance = PageClass(parent=self, color="#9dcef2")
            self.pages[PageClass] = page_instance
            page_instance.grid(row=1, column=1, sticky="nsew")
        
        # Display collections page at the start
        self.show_page(CollectionsPage)

    def show_sidebar(self):
        """Display the common sidebar for all pages except settings."""
        for widget in self.sidebar_frame.winfo_children():
            widget.destroy()

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="AProject", font=ctk.CTkFont(size=20, weight="bold"), padx=10)
        self.logo_label.pack(padx=(23, 10), pady=(12, 14), anchor="w")

        self.sidebar_button_1 = ctk.CTkButton(
            self.sidebar_frame,
            text="+ Collection  ",
            corner_radius=0,
            anchor="center",
            font=ctk.CTkFont(size=17), 
            height=50,
            command=self.add_new_button
        )
        self.sidebar_button_1.pack(fill="x", pady=2)

        # Create Scrollable frame for collections here
        self.scrollable_frame = ctk.CTkScrollableFrame(self.sidebar_frame)
        self.scrollable_frame.pack(fill="both", expand=True)

        # Intermediate frame inside the scrollable frame
        self.inner_frame = tk.Frame(self.scrollable_frame, bg='#9dcef2')
        self.inner_frame.pack(fill="both", expand=True)

        # Populate the inner frame with the saved collections from the database
        self.populate_collections_from_db()

    def configure_app(self):
        """Configure the main app window."""
        self.title("AProject")
        self.geometry(f"{1100}x{580}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def create_sidebar_frame(self):
        """Create the sidebar frame."""
        self.sidebar_frame = ctk.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)

    def create_navbar(self):
        """Create the navbar with its buttons."""
        self.navbar_frame = ctk.CTkFrame(self, height=53.5, corner_radius=0)
        self.navbar_frame.grid(row=0, column=1, sticky="new", columnspan=2)
        self.navbar_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        navbar_button_style = {"corner_radius": 0, "height": 53.5, "anchor": "center"}
        buttons_data = [
            ("Collections", lambda: self.show_page(CollectionsPage)),
            ("Import", lambda: self.show_page(ImportPage)),
            ("USB", lambda: self.show_page(UsbPage)),
            ("Settings", lambda: self.show_page(SettingsPage))
        ]

        self.buttons = []
        for index, (label, command) in enumerate(buttons_data):
            button = ctk.CTkButton(self.navbar_frame, text=label, command=command, **navbar_button_style, font=ctk.CTkFont(size=17, weight="bold"))
            button.grid(row=0, column=index, sticky="nsew")
            self.buttons.append(button)

        button_width = (self.winfo_screenwidth() - self.sidebar_frame.winfo_width()) // 4
        for button in self.buttons:
            button.configure(width=button_width)

    def add_new_button(self):
        """Add a new button to the sidebar with an entry widget for user input and save it to the database."""

        entry_button = ctk.CTkEntry(
            self.inner_frame,
            font=ctk.CTkFont(size=15),
            corner_radius=0
        )
    
        # Always pack before the first child to keep it at the top
        entry_button.pack(fill="x", pady=2, before=self.inner_frame.winfo_children()[0])
        
        entry_button.focus()
        entry_button.bind("<Return>", lambda event: self.save_button(entry_button))

    def save_button(self, entry_widget):
        """Save the new collection button and its data."""
        name = entry_widget.get().strip()
        if name:
            button_data = {
                "name": name,
                "content": []
            }
            self.db.add_button(name, button_data)
        
            # Destroy the entry widget
            entry_widget.destroy()

            # Repopulate collections which will now be in sorted order
            self.populate_collections_from_db()

    def populate_collections_from_db(self):
        """Populate the scrollable frame with buttons from the database."""
        collections = self.db.data["Collections"]
        # Sort collections by their names
        sorted_collections = sorted(collections.items(), key=lambda x: x[0].lower())

        # First, clear all existing buttons
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Populate sorted collections
        for name, data in sorted_collections:
            button = ctk.CTkButton(
                self.inner_frame,  
                text=name,
                corner_radius=0,
                anchor="center",
                font=ctk.CTkFont(size=15),
                height=50
            )
            button.pack(fill="x", pady=2)

    def clear_canvas(self):
        """Clear the canvas and its contents."""
        for widget in self.canvas.winfo_children():
            widget.destroy()
        self.canvas.delete("all")
        
    def show_collections(self):
        self.show_sidebar()
        # Create a canvas for the masonry layout
        self.canvas = tk.Canvas(self, bg='#9dcef2')
        self.canvas.grid(row=1, column=1, sticky="nsew")

        # Add a scrollbar to the canvas
        self.scrollbar = ctk.CTkScrollbar(self.canvas)
        self.scrollbar.grid(row=1, column=2, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold the widgets
        self.masonry_frame = tk.Frame(self.canvas, bg='#9dcef2')
        self.canvas.create_window((0, 0), window=self.masonry_frame, anchor="nw")

        self.masonry_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Bind the mouse wheel event to the masonry_frame and the canvas
        self.masonry_frame.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Configure>", self.adjust_masonry_layout)

        # Sample widgets for the masonry layout
        self.widgets = []
        for i in range(20):
            frame = tk.Frame(self.masonry_frame, width=200, height=150, bg=f"#{i*5%256:02x}{i*10%256:02x}{i*15%256:02x}")
            frame.pack(padx=10, pady=10)
            frame.bind("<MouseWheel>", self.on_mousewheel)
            self.widgets.append(frame)

    def adjust_masonry_layout(self, event=None):
        '''Adjust the masonry layout based on the canvas width.'''
        widget_width = 210
        canvas_width = self.canvas.winfo_width()
        num_columns = max(1, canvas_width // widget_width)

        for widget in self.widgets:
            widget.pack_forget()

        for i, widget in enumerate(self.widgets):
            widget.grid(row=i//num_columns, column=i%num_columns, padx=10, pady=10)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120), "units")

    def show_import(self):
        self.show_sidebar()
        self.clear_canvas()
        self.scrollbar.grid_forget()

    def show_usb(self):
        self.show_sidebar()
        self.clear_canvas()
        self.scrollbar.grid_forget()

    def show_settings(self):
        # Clear the sidebar for the settings page
        for widget in self.sidebar_frame.winfo_children():
            widget.destroy()

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="AProject", font=ctk.CTkFont(size=20, weight="bold"), padx=10)
        self.logo_label.pack(padx=(23, 10), pady=(12, 14), anchor="w")
        self.clear_canvas()
        self.scrollbar.grid_forget()

    def show_page(self, page_class):
        page = self.pages[page_class]
        page.tkraise()