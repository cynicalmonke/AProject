import tkinter as tk
import customtkinter as ctk
from ..data.database import Database
import tkinter.messagebox as messagebox

# Creating the Page base class
class Page(tk.Frame):
    def __init__(self, parent=None, color="#474747"):     
        super().__init__(parent, bg=color)
        self.parent = parent

    def center_messagebox(self, mb):
        # Update the main window to ensure it's been drawn and has a size
        self.parent.update_idletasks()
        mb.update_idletasks()

        # Calculate the center position
        x = (self.parent.winfo_width() - mb.winfo_width()) // 2 + self.parent.winfo_x()
        y = (self.parent.winfo_height() - mb.winfo_height()) // 2 + self.parent.winfo_y()

        # Set the position of the messagebox
        mb.geometry(f"+{x}+{y}")

    def show_logo_label(self):
        logo_label = ctk.CTkLabel(self.parent.sidebar_frame, text="AProject", font=ctk.CTkFont(size=20, weight="bold"), padx=10)
        logo_label.grid(row=0, column=0, columnspan=2, padx=(23, 10), pady=(12, 14), sticky="w")


    def show_sidebar(self):
        """Display the common sidebar for all pages except settings."""

        for widget in self.parent.sidebar_frame.winfo_children():
            widget.destroy()

        # Configure the sidebar_frame for two columns
        self.parent.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.parent.sidebar_frame.grid_columnconfigure(1, weight=100)
        # Configure the sidebar_frame for three rows
        self.parent.sidebar_frame.grid_rowconfigure(0, weight=0)  # Logo label
        self.parent.sidebar_frame.grid_rowconfigure(1, weight=0)  # Buttons
        self.parent.sidebar_frame.grid_rowconfigure(2, weight=1)  # Scrollable frame (should expand)

        # Display the logo label
        self.show_logo_label()

        sidebar_button_add = ctk.CTkButton(
            self.parent.sidebar_frame,
            text="+ Collection",
            corner_radius=0,
            anchor="center",
            font=ctk.CTkFont(size=17), 
            height=50,
            command=self.add_new_button
        )
        sidebar_button_add.grid(row=1, column=0, sticky="nsew", pady=2)

        trashcan_icon = tk.PhotoImage(file="app/gui/icons/trash-2-24.png")

        sidebar_button_del = ctk.CTkButton(
            self.parent.sidebar_frame,
            text="",
            image=trashcan_icon,
            corner_radius=0,
            anchor="center",
            height=50,
            fg_color="red",
            command=self.delete_button
        )
        sidebar_button_del.grid(row=1, column=1, sticky="nsew", pady=2)

        # Create Scrollable frame for collections here
        self.scrollable_frame = ctk.CTkScrollableFrame(self.parent.sidebar_frame)
        # scrollable_frame.pack(fill="both", expand=True)
        self.scrollable_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=2)

        # Intermediate frame inside the scrollable frame
        self.inner_frame = tk.Frame(self.scrollable_frame, bg='#474747')
        self.inner_frame.pack(fill="both", expand=True)

        # Populate the inner frame with the saved collections from the database
        self.populate_collections_from_db(self.inner_frame)

    def populate_collections_from_db(self, inner_frame):
        """Populate the scrollable frame with buttons from the database."""
        collections = self.parent.db.data["Collections"]
        # Sort collections by their names
        sorted_collections = sorted(collections.items(), key=lambda x: x[0].lower())

        # First, clear all existing buttons
        for widget in inner_frame.winfo_children():
            widget.destroy()

        # Populate sorted collections
        for name, data in sorted_collections:
            button = ctk.CTkButton(
                inner_frame,  
                text=name,
                corner_radius=0,
                anchor="center",
                font=ctk.CTkFont(size=15),
                height=50
            )
            button.custom_text = name  # Storing the button text in a custom attribute
            button.pack(fill="x", pady=2)
            button.bind("<Button-1>", lambda event, btn=button, n=name: self.set_selected(n, btn))

            # Check if this button is the selected one
            if name == self.parent.selected:
                button.configure(fg_color="#174f7a")

    def set_selected(self, name, clicked_button):
        """Set the given name to the selected attribute and alter the button's color."""

        # Let's get all the CTkButton children first
        button_children = [btn for btn in self.inner_frame.winfo_children() if isinstance(btn, ctk.CTkButton)]

        # Among the button children, find the one that matches our selected button text
        prev_button = next((btn for btn in button_children if btn.custom_text == self.parent.selected), None)
    
        # Reset the previously selected button color
        if prev_button:
            prev_button.configure(fg_color="#1f6aa5")
    
        # Set the new selected button
        self.parent.selected = name
        print(self.parent.selected)
        clicked_button.configure(fg_color="#174f7a")

        
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
            self.parent.db.add_button(name, button_data)
        
            # Destroy the entry widget
            entry_widget.destroy()

            # Repopulate collections which will now be in sorted order
            self.populate_collections_from_db(self.inner_frame)
    
    def delete_button(self):
        if self.parent.selected is not None:
            # Ask for confirmation to delete the selected collection
            mb = messagebox.askyesno("Delete Collection", f"Are you sure you want to delete \n{self.parent.selected} collection?")
            self.center_messagebox(mb)
            if mb.result:
                # Delete the button from the database
                self.parent.db.remove_button(self.parent.selected)
                # Repopulate collections which will now be in sorted order
                self.populate_collections_from_db(self.inner_frame)
                self.parent.selected = None
        else:
            # Inform the user to select a collection first
            mb = messagebox.showinfo("Delete Collection", "Please select a collection to delete.")
            self.center_messagebox(mb)


# Creating subclasses for each page
class CollectionsPage(Page):
    def __init__(self, parent=None, color="#474747"):
        print("Initializing CollectionsPage")
        super().__init__(parent, color)
        self.show_sidebar()
        self.after(100, lambda: parent._bind_to_mousewheel(self.scrollable_frame))
        
        # Add widgets for the collections page here
        self.create_masonry_layout()
        self.after_idle(self.initial_layout_pass)
        
    def initial_layout_pass(self):
        """Perform layout after the window is displayed and the sizes are known."""
        self.adjust_masonry_layout(self.canvas.winfo_width())
        
    def create_masonry_layout(self):
        # Create a canvas for the masonry layout
        self.canvas = tk.Canvas(self, bg=self['bg'])
        self.canvas.pack(side="left", fill="both", expand=True)

        # Configure the scrollbar properly
        self.scrollbar = ctk.CTkScrollbar(self, command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold the widgets
        self.masonry_frame = tk.Frame(self.canvas, bg=self['bg'])
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.masonry_frame, anchor="nw")

        self.masonry_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Populate with widgets or call a function to populate it
        self.populate_masonry_frame()
        
        self.parent._bind_to_mousewheel(self.masonry_frame)
        # self.parent._bind_to_mousewheel(self.canvas)
        

    def on_frame_configure(self, event=None):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        '''Adjust the masonry layout based on the canvas width.'''
        canvas_width = event.width
        self.adjust_masonry_layout(canvas_width)

    def adjust_masonry_layout(self, canvas_width):
        '''Adjust the masonry layout based on the canvas width.'''
        widget_width = 210  # widget width + padx
        num_columns = max(1, canvas_width // widget_width)
        # Adjust the layout of widgets based on the number of columns
        for widget in self.widgets:
            widget.grid_forget()  # Forget the pack to reset the layout
        for i, widget in enumerate(self.widgets):
            widget.grid(row=i // num_columns, column=i % num_columns, padx=10, pady=10)

    def populate_masonry_frame(self):
        # Example of populating the frame with widgets
        self.widgets = []
        for i in range(20):
            frame = tk.Frame(self.masonry_frame, width=200, height=200, bg=f"#{i*12:02x}{i*12:02x}{i*12:02x}")
            frame.grid(padx=10, pady=10)
            self.widgets.append(frame)

class ImportPage(Page):
    def __init__(self, parent=None, color="#474747"):
        print("Initializing ImportPage")
        super().__init__(parent, color)
        self.show_sidebar()
        # Add widgets for the import page here

class UsbPage(Page):
    def __init__(self, parent=None, color="#474747"):
        print("Initializing UsbPage")
        super().__init__(parent, color)
        self.show_sidebar()
        # Add widgets for the usb page here

class SettingsPage(Page):
    def __init__(self, parent=None, color="#474747"):
        print("Initializing SettingsPage")
        super().__init__(parent, color)
        # Add widgets for the settings page here

    def show_sidebar(self):
        """Override the show_sidebar method to do nothing for the SettingsPage."""
        for widget in self.parent.sidebar_frame.winfo_children():
            widget.destroy()

        self.show_logo_label()

class App(tk.Tk):  # Changed from ctk.CTk to tk.Tk
    def __init__(self):
        super().__init__()
        self.configure(bg="#474747")
        self.db = Database()
        self.configure_app()
        self.create_sidebar_frame()
        self.create_navbar()
        self.selected = None

        # Storing the pages in a dictionary
        self.pages = {}
        for PageClass in (CollectionsPage, ImportPage, UsbPage, SettingsPage):
            page_instance = PageClass(parent=self)
            self.pages[PageClass] = page_instance
            page_instance.grid(row=1, column=1, sticky="nsew")
        
        # Display collections page at the start
        self.show_page(CollectionsPage)
        
        # Bind the mousewheel to the root window
        self.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        widget = event.widget
        if hasattr(widget, 'yview'):
            delta = -1 * (event.delta // 120) if self.tk.call('tk', 'windowingsystem') == 'win32' else event.delta // 120
            widget.yview_scroll(int(delta), "units")

    def _bind_to_mousewheel(self, widget):
        print(f"Binding to mousewheel: {widget}")
        widget.bind("<Enter>", lambda event: self._attach_mousewheel_to_widget(widget))
        widget.bind("<Leave>", lambda event: self._detach_mousewheel_from_widget(widget))

    def _attach_mousewheel_to_widget(self, widget):
        child_widgets = widget.winfo_children()
        for child_widget in child_widgets:
            if hasattr(child_widget, 'yview'):
                self._bind_to_mousewheel(child_widget)
            self._attach_mousewheel_to_widget(child_widget)
        widget.bind_all("<MouseWheel>", self._on_mousewheel)

    def _detach_mousewheel_from_widget(self, widget):
        widget.unbind_all("<MouseWheel>")
        child_widgets = widget.winfo_children()
        for child_widget in child_widgets:
            self._detach_mousewheel_from_widget(child_widget)
        
    def configure_app(self):
        """Configure the main app window."""
        self.title("AProject")
        self.geometry(f"{1100}x{580}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        # Prevent the window from being resized
        self.resizable(False, False)

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
        ("Collections", lambda: (print("Collections button clicked"), self.show_page(CollectionsPage))),
        ("Import", lambda: (print("Import button clicked"), self.show_page(ImportPage))),
        ("USB", lambda: (print("USB button clicked"), self.show_page(UsbPage))),
        ("Settings", lambda: (print("Settings button clicked"), self.show_page(SettingsPage)))
        ]

        self.buttons = []
        for index, (label, command) in enumerate(buttons_data):
            button = ctk.CTkButton(self.navbar_frame, text=label, command=command, **navbar_button_style, font=ctk.CTkFont(size=17, weight="bold"))
            button.grid(row=0, column=index, sticky="nsew")
            self.buttons.append(button)

        button_width = (self.winfo_screenwidth() - self.sidebar_frame.winfo_width()) // 4
        for button in self.buttons:
            button.configure(width=button_width)

    def show_page(self, page_class):
        print(f"Showing page: {page_class.__name__}")
        page = self.pages[page_class]
        page.show_sidebar()
        page.tkraise()
