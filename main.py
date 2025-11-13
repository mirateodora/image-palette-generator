import tkinter as tk
from tkinter import filedialog, messagebox, font as tkfont

import matplotlib.pyplot as plt
from PIL import Image, ImageTk

from palette_utils import *


class PaletteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Palette Generator")
        self.root.geometry("800x700")
        self.root.configure(background="#1a1a2e")

        # Color scheme
        self.bg_primary = "#1a1a2e"
        self.bg_secondary = "#16213e"
        self.accent = "#0f3460"
        self.highlight = "#e94560"
        self.text_light = "#ffffff"
        self.text_muted = "#a0a0a0"

        self.img_path = None
        self.img_tk = None
        self.loading_animation_id = None
        self.loading_angle = 0

        # Custom fonts
        try:
            self.title_font = tkfont.Font(family="Segoe UI", size=24, weight="bold")
            self.body_font = tkfont.Font(family="Segoe UI", size=10)
            self.button_font = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        except:
            self.title_font = tkfont.Font(size=24, weight="bold")
            self.body_font = tkfont.Font(size=10)
            self.button_font = tkfont.Font(size=11, weight="bold")

        self.create_ui()

    def create_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_primary)
        header_frame.pack(fill="x", pady=(20, 10))

        title = tk.Label(
            header_frame,
            text="🎨 Palette Generator",
            font=self.title_font,
            bg=self.bg_primary,
            fg=self.text_light
        )
        title.pack()

        subtitle = tk.Label(
            header_frame,
            text="Extract beautiful color palettes from your images",
            font=self.body_font,
            bg=self.bg_primary,
            fg=self.text_muted
        )
        subtitle.pack()

        # Main content frame
        content_frame = tk.Frame(self.root, bg=self.bg_primary)
        content_frame.pack(expand=True, fill="both", padx=30, pady=10)

        # Upload button with modern styling
        self.upload_btn = tk.Button(
            content_frame,
            text="📁 Choose Image",
            command=self.upload_image,
            font=self.button_font,
            bg=self.highlight,
            fg=self.text_light,
            activebackground="#c73854",
            activeforeground=self.text_light,
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=12,
            borderwidth=0
        )
        self.upload_btn.pack(pady=(0, 20))
        self.add_hover_effect(self.upload_btn, self.highlight, "#c73854")

        # Canvas container with border
        canvas_container = tk.Frame(content_frame, bg=self.bg_secondary, relief="flat", borderwidth=0)
        canvas_container.pack(pady=10)

        canvas_border = tk.Frame(canvas_container, bg=self.accent, padx=2, pady=2)
        canvas_border.pack()

        self.canvas = tk.Canvas(
            canvas_border,
            width=600,
            height=300,
            bg=self.bg_secondary,
            highlightthickness=0,
            relief="flat"
        )
        self.canvas.pack()

        # Placeholder text
        self.placeholder_text = self.canvas.create_text(
            300, 150,
            text="No image selected\nClick 'Choose Image' to get started",
            font=self.body_font,
            fill=self.text_muted,
            justify="center"
        )

        # Controls frame
        controls_frame = tk.Frame(content_frame, bg=self.bg_primary)
        controls_frame.pack(pady=20)

        # Color slider with label
        slider_label = tk.Label(
            controls_frame,
            text="Number of Colors",
            font=self.body_font,
            bg=self.bg_primary,
            fg=self.text_light
        )
        slider_label.grid(row=0, column=0, padx=10)

        self.color_value_label = tk.Label(
            controls_frame,
            text="5",
            font=self.button_font,
            bg=self.accent,
            fg=self.text_light,
            width=3,
            padx=10,
            pady=5
        )
        self.color_value_label.grid(row=0, column=1, padx=10)

        self.color_slider = tk.Scale(
            controls_frame,
            from_=3,
            to=10,
            orient="horizontal",
            command=self.update_slider_label,
            bg=self.bg_primary,
            fg=self.text_light,
            troughcolor=self.accent,
            highlightthickness=0,
            sliderrelief="flat",
            activebackground=self.highlight,
            length=200
        )
        self.color_slider.set(5)
        self.color_slider.grid(row=1, column=0, columnspan=2, pady=10)

        # Generate button
        self.generate_btn = tk.Button(
            content_frame,
            text="✨ Generate Palette",
            command=self.generate_palette,
            font=self.button_font,
            bg=self.accent,
            fg=self.text_light,
            activebackground="#0a2342",
            activeforeground=self.text_light,
            relief="flat",
            cursor="hand2",
            padx=40,
            pady=12,
            borderwidth=0
        )
        self.generate_btn.pack(pady=10)
        self.add_hover_effect(self.generate_btn, self.accent, "#0a2342")

        # Hex output frame
        output_frame = tk.Frame(content_frame, bg=self.bg_secondary, padx=15, pady=15)
        output_frame.pack(pady=10, fill="x")

        output_label = tk.Label(
            output_frame,
            text="Color Codes:",
            font=self.body_font,
            bg=self.bg_secondary,
            fg=self.text_light
        )
        output_label.pack(anchor="w")

        self.hex_output = tk.Text(
            output_frame,
            height=3,
            width=60,
            font=("Courier New", 10),
            bg=self.accent,
            fg=self.text_light,
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=10,
            insertbackground=self.text_light
        )
        self.hex_output.pack(fill="x", pady=(5, 0))

    def add_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to buttons"""
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))

    def update_slider_label(self, value):
        """Update the slider value label"""
        self.color_value_label.config(text=str(int(float(value))))

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[('Image Files', '*.png *.jpg *.jpeg *.bmp *.gif')]
        )
        if file_path:
            self.img_path = file_path
            self.show_preview(file_path)

    def show_preview(self, file_path):
        self.canvas.delete("all")
        img = Image.open(file_path)
        img.thumbnail((580, 280))
        self.img_tk = ImageTk.PhotoImage(img)

        # Center the image
        x = (600 - img.width) // 2
        y = (300 - img.height) // 2
        self.canvas.create_image(x + img.width // 2, y + img.height // 2, image=self.img_tk)

    def generate_palette(self):
        if not self.img_path:
            messagebox.showerror("Error", "Please select an image first")
            return

        # Show loading animation
        self.show_loading()

        # Disable buttons during processing
        self.generate_btn.config(state="disabled")
        self.upload_btn.config(state="disabled")

        # Schedule the actual palette generation after a brief delay
        # This allows the loading animation to render
        self.root.after(50, self.process_palette)

    def process_palette(self):
        number_of_colors = int(self.color_slider.get())
        try:
            colors = extract_colors(self.img_path, number_of_colors)
        except Exception as e:
            self.stop_loading()
            self.generate_btn.config(state="normal")
            self.upload_btn.config(state="normal")
            messagebox.showerror("Error", f"Failed to extract colors: {str(e)}")
            return

        # Stop loading animation
        self.stop_loading()

        # Re-enable buttons
        self.generate_btn.config(state="normal")
        self.upload_btn.config(state="normal")

        self.canvas.delete("all")

        # Draw color swatches with rounded appearance
        swatch_width = 600 // number_of_colors
        hex_codes = []

        for i, color in enumerate(colors):
            hex_code = rgb_to_hex(color)
            hex_codes.append(hex_code)
            x0, x1 = i * swatch_width, (i + 1) * swatch_width

            # Create swatch
            self.canvas.create_rectangle(
                x0, 50, x1, 250,
                fill=hex_code,
                outline='',
                width=0
            )

            # Add hex code label with background
            label_y = 270
            self.canvas.create_text(
                (x0 + x1) // 2, label_y,
                text=hex_code,
                font=("Courier New", 9, "bold"),
                fill=self.text_light
            )

        # Update hex output
        self.hex_output.delete(1.0, tk.END)
        self.hex_output.insert(tk.END, " | ".join(hex_codes))

    def show_loading(self):
        """Display loading animation"""
        self.canvas.delete("all")
        self.loading_angle = 0
        self.animate_loading()

    def animate_loading(self):
        """Animate a spinning loader"""
        self.canvas.delete("loader")

        # Draw spinning arc
        center_x, center_y = 300, 150
        radius = 40

        # Create multiple arcs for a smooth spinner effect
        for i in range(3):
            start_angle = self.loading_angle + (i * 120)
            self.canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle,
                extent=100,
                outline=self.highlight,
                width=4,
                style="arc",
                tags="loader"
            )

        # Loading text
        self.canvas.create_text(
            center_x, center_y + 70,
            text="Extracting colors...",
            font=self.body_font,
            fill=self.text_muted,
            tags="loader"
        )

        # Update angle and schedule next frame
        self.loading_angle = (self.loading_angle + 10) % 360
        self.loading_animation_id = self.root.after(10, self.animate_loading)

    def stop_loading(self):
        """Stop the loading animation"""
        if self.loading_animation_id:
            self.root.after_cancel(self.loading_animation_id)
            self.loading_animation_id = None


if __name__ == "__main__":
    root = tk.Tk()
    app = PaletteGenerator(root)
    root.mainloop()