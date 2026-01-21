import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk
import json
import os


class ColorPaletteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Color Palette Generator")
        self.root.geometry("1100x850")
        self.root.configure(bg="#f0f0f0")

        # Color variables
        self.selected_color = "#000000"
        self.custom_colors = []
        self.color_history = []

        # Predefined color palettes
        self.palettes = {
            "Material Design": ["#F44336", "#E91E63", "#9C27B0", "#673AB7", "#3F51B5",
                                "#2196F3", "#03A9F4", "#00BCD4", "#009688", "#4CAF50"],
            "Pastel": ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF",
                       "#FFB3FF", "#FFCCE5", "#D5AAFF", "#B5EAD7", "#C7CEEA"],
            "Warm": ["#FF6B6B", "#FF8E53", "#FFD166", "#06D6A0", "#118AB2",
                     "#EF476F", "#FFD166", "#06D6A0", "#073B4C", "#118AB2"],
            "Cool": ["#264653", "#2A9D8F", "#E9C46A", "#F4A261", "#E76F51",
                     "#1D3557", "#457B9D", "#A8DADC", "#F1FAEE", "#E63946"],
            "Rainbow": ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF",
                        "#4B0082", "#9400D3", "#FF1493", "#00FFFF", "#FFD700"]
        }

        self.setup_ui()

    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(main_frame, bg="#667eea")
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title_label = tk.Label(header_frame, text="🎨 COLOR PALETTE GENERATOR",
                               font=("Arial", 28, "bold"), bg="#667eea", fg="white")
        title_label.pack(pady=25)

        subtitle_label = tk.Label(header_frame,
                                  text="Create, save and export beautiful color palettes",
                                  font=("Arial", 12), bg="#667eea", fg="white")
        subtitle_label.pack(pady=(0, 15))

        # Content area
        content_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=1)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel - Color selection
        left_panel = tk.Frame(content_frame, bg="white", width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        # Right panel - Palette display
        right_panel = tk.Frame(content_frame, bg="white")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Left Panel Content
        tk.Label(left_panel, text="COLOR PICKER", font=("Arial", 16, "bold"),
                 bg="white", fg="#333").pack(anchor=tk.W, pady=(0, 15))

        # Color picker button
        color_picker_btn = tk.Button(left_panel, text="🎨 Pick Color",
                                     font=("Arial", 12, "bold"), bg="#4CAF50",
                                     fg="white", padx=20, pady=10,
                                     command=self.pick_color)
        color_picker_btn.pack(pady=10)

        # Current color display
        self.color_display = tk.Frame(left_panel, bg=self.selected_color,
                                      height=50, width=200, relief=tk.SUNKEN, bd=2)
        self.color_display.pack(pady=20)

        self.color_label = tk.Label(left_panel, text=self.selected_color,
                                    font=("Arial", 12, "bold"), bg="white")
        self.color_label.pack()

        # RGB sliders
        tk.Label(left_panel, text="RGB ADJUSTMENT", font=("Arial", 14, "bold"),
                 bg="white", fg="#333").pack(anchor=tk.W, pady=(30, 10))

        # Red slider
        tk.Label(left_panel, text="Red:", font=("Arial", 10), bg="white").pack(anchor=tk.W)
        self.red_slider = tk.Scale(left_panel, from_=0, to=255, orient=tk.HORIZONTAL,
                                   length=200, command=self.update_from_sliders)
        self.red_slider.set(0)
        self.red_slider.pack(pady=5)

        # Green slider
        tk.Label(left_panel, text="Green:", font=("Arial", 10), bg="white").pack(anchor=tk.W)
        self.green_slider = tk.Scale(left_panel, from_=0, to=255, orient=tk.HORIZONTAL,
                                     length=200, command=self.update_from_sliders)
        self.green_slider.set(0)
        self.green_slider.pack(pady=5)

        # Blue slider
        tk.Label(left_panel, text="Blue:", font=("Arial", 10), bg="white").pack(anchor=tk.W)
        self.blue_slider = tk.Scale(left_panel, from_=0, to=255, orient=tk.HORIZONTAL,
                                    length=200, command=self.update_from_sliders)
        self.blue_slider.set(0)
        self.blue_slider.pack(pady=5)

        # Add to palette button
        add_btn = tk.Button(left_panel, text="➕ Add to Palette",
                            font=("Arial", 12), bg="#2196F3", fg="white",
                            command=self.add_to_palette, padx=15, pady=8)
        add_btn.pack(pady=20)

        # Clear palette button
        clear_btn = tk.Button(left_panel, text="🗑️ Clear Palette",
                              font=("Arial", 10), bg="#f44336", fg="white",
                              command=self.clear_palette)
        clear_btn.pack(pady=5)

        # Right Panel Content
        # Palette selector
        palette_frame = tk.Frame(right_panel, bg="white")
        palette_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(palette_frame, text="PREDEFINED PALETTES",
                 font=("Arial", 16, "bold"), bg="white", fg="#333").pack(anchor=tk.W)

        # Palette buttons
        palette_btn_frame = tk.Frame(palette_frame, bg="white")
        palette_btn_frame.pack(fill=tk.X, pady=10)

        for palette_name in self.palettes.keys():
            btn = tk.Button(palette_btn_frame, text=palette_name,
                            font=("Arial", 10), bg="#E0E0E0",
                            command=lambda name=palette_name: self.load_palette(name))
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Current palette display
        tk.Label(right_panel, text="YOUR PALETTE", font=("Arial", 16, "bold"),
                 bg="white", fg="#333").pack(anchor=tk.W, pady=(0, 10))

        self.palette_display = tk.Frame(right_panel, bg="white")
        self.palette_display.pack(fill=tk.BOTH, expand=True)

        # Color information
        info_frame = tk.Frame(right_panel, bg="white", relief=tk.GROOVE, bd=1)
        info_frame.pack(fill=tk.X, pady=20)

        tk.Label(info_frame, text="COLOR INFORMATION", font=("Arial", 14, "bold"),
                 bg="white", fg="#333").pack(anchor=tk.W, padx=10, pady=10)

        self.info_text = tk.Text(info_frame, height=6, width=60, font=("Courier", 10))
        self.info_text.pack(padx=10, pady=(0, 10))
        self.info_text.insert(tk.END, "No colors in palette yet.\nAdd colors using the color picker.")
        self.info_text.config(state=tk.DISABLED)

        # Export buttons
        export_frame = tk.Frame(right_panel, bg="white")
        export_frame.pack(fill=tk.X, pady=10)

        export_btn = tk.Button(export_frame, text="💾 Export as JSON",
                               font=("Arial", 12, "bold"), bg="#9C27B0", fg="white",
                               command=self.export_json, padx=20, pady=10)
        export_btn.pack(side=tk.LEFT, padx=5)

        export_css_btn = tk.Button(export_frame, text="🎨 Export as CSS",
                                   font=("Arial", 12, "bold"), bg="#FF9800", fg="white",
                                   command=self.export_css, padx=20, pady=10)
        export_css_btn.pack(side=tk.LEFT, padx=5)

        export_image_btn = tk.Button(export_frame, text="🖼️ Export as Image",
                                     font=("Arial", 12, "bold"), bg="#00BCD4", fg="white",
                                     command=self.export_image, padx=20, pady=10)
        export_image_btn.pack(side=tk.LEFT, padx=5)

        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN,
                                   anchor=tk.W, bg="#E0E0E0")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def pick_color(self):
        """Open color picker dialog"""
        color = colorchooser.askcolor(title="Choose a color", initialcolor=self.selected_color)
        if color[1]:  # User didn't cancel
            self.selected_color = color[1]
            self.update_color_display()

    def update_color_display(self):
        """Update the color display and RGB sliders"""
        # Update display frame
        self.color_display.config(bg=self.selected_color)

        # Update label
        self.color_label.config(text=self.selected_color)

        # Update RGB sliders
        if self.selected_color.startswith("#"):
            r = int(self.selected_color[1:3], 16)
            g = int(self.selected_color[3:5], 16)
            b = int(self.selected_color[5:7], 16)

            self.red_slider.set(r)
            self.green_slider.set(g)
            self.blue_slider.set(b)

    def update_from_sliders(self, *args):
        """Update color from RGB sliders"""
        r = self.red_slider.get()
        g = self.green_slider.get()
        b = self.blue_slider.get()

        self.selected_color = f"#{r:02x}{g:02x}{b:02x}".upper()
        self.color_display.config(bg=self.selected_color)
        self.color_label.config(text=self.selected_color)

    def add_to_palette(self):
        """Add current color to palette"""
        if self.selected_color not in self.custom_colors:
            self.custom_colors.append(self.selected_color)
            self.update_palette_display()
            self.update_info_text()
            self.status_bar.config(text=f"Added {self.selected_color} to palette")

    def clear_palette(self):
        """Clear the current palette"""
        self.custom_colors = []
        self.update_palette_display()
        self.update_info_text()
        self.status_bar.config(text="Palette cleared")

    def update_palette_display(self):
        """Update the palette display area"""
        # Clear existing widgets
        for widget in self.palette_display.winfo_children():
            widget.destroy()

        if not self.custom_colors:
            empty_label = tk.Label(self.palette_display, text="No colors in palette",
                                   font=("Arial", 12), bg="white", fg="gray")
            empty_label.pack(pady=50)
            return

        # Create a grid of color swatches
        rows = (len(self.custom_colors) + 4) // 5  # 5 columns
        for i in range(rows):
            row_frame = tk.Frame(self.palette_display, bg="white")
            row_frame.pack(fill=tk.X, pady=5)

            for j in range(5):
                idx = i * 5 + j
                if idx < len(self.custom_colors):
                    color = self.custom_colors[idx]

                    # Create color swatch
                    swatch_frame = tk.Frame(row_frame, width=80, height=80,
                                            bg=color, relief=tk.RAISED, bd=2)
                    swatch_frame.pack(side=tk.LEFT, padx=5)
                    swatch_frame.pack_propagate(False)  # Keep fixed size

                    # Add color label
                    label = tk.Label(swatch_frame, text=color, bg=color,
                                     fg=self.get_contrast_color(color),
                                     font=("Arial", 8))
                    label.pack(side=tk.BOTTOM, fill=tk.X)

                    # Add click event to select color
                    swatch_frame.bind("<Button-1>", lambda e, c=color: self.select_swatch_color(c))
                    label.bind("<Button-1>", lambda e, c=color: self.select_swatch_color(c))

                    # Add delete button
                    delete_btn = tk.Button(swatch_frame, text="✕",
                                           font=("Arial", 8, "bold"),
                                           bg=color, fg=self.get_contrast_color(color),
                                           command=lambda idx=idx: self.delete_color(idx))
                    delete_btn.place(relx=0.8, rely=0.1, anchor=tk.NE)

    def get_contrast_color(self, hex_color):
        """Get black or white for best contrast"""
        if hex_color.startswith("#"):
            hex_color = hex_color[1:]

        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        # Calculate luminance
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return "white" if luminance < 0.5 else "black"

    def select_swatch_color(self, color):
        """Select color from swatch"""
        self.selected_color = color
        self.update_color_display()
        self.status_bar.config(text=f"Selected {color}")

    def delete_color(self, index):
        """Delete color from palette"""
        if 0 <= index < len(self.custom_colors):
            deleted_color = self.custom_colors.pop(index)
            self.update_palette_display()
            self.update_info_text()
            self.status_bar.config(text=f"Removed {deleted_color}")

    def update_info_text(self):
        """Update color information text"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)

        if not self.custom_colors:
            self.info_text.insert(tk.END, "No colors in palette yet.\nAdd colors using the color picker.")
        else:
            self.info_text.insert(tk.END, "Colors in palette:\n")
            self.info_text.insert(tk.END, "=" * 40 + "\n")

            for i, color in enumerate(self.custom_colors, 1):
                # Convert hex to RGB
                if color.startswith("#"):
                    r = int(color[1:3], 16)
                    g = int(color[3:5], 16)
                    b = int(color[5:7], 16)

                    self.info_text.insert(tk.END,
                                          f"{i:2d}. {color}  RGB: ({r:3d}, {g:3d}, {b:3d})\n")

        self.info_text.config(state=tk.DISABLED)

    def load_palette(self, palette_name):
        """Load a predefined palette"""
        if palette_name in self.palettes:
            self.custom_colors = self.palettes[palette_name].copy()
            self.update_palette_display()
            self.update_info_text()
            self.status_bar.config(text=f"Loaded '{palette_name}' palette")

    def export_json(self):
        """Export palette as JSON file"""
        if not self.custom_colors:
            messagebox.showwarning("No Colors", "Please add colors to the palette first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="color_palette.json"
        )

        if file_path:
            palette_data = {
                "name": "My Color Palette",
                "colors": self.custom_colors,
                "count": len(self.custom_colors),
                "metadata": {
                    "created_with": "Color Palette Generator",
                    "colors": []
                }
            }

            # Add color details
            for color in self.custom_colors:
                if color.startswith("#"):
                    r = int(color[1:3], 16)
                    g = int(color[3:5], 16)
                    b = int(color[5:7], 16)

                    palette_data["metadata"]["colors"].append({
                        "hex": color,
                        "rgb": [r, g, b],
                        "contrast": self.get_contrast_color(color)
                    })

            try:
                with open(file_path, 'w') as f:
                    json.dump(palette_data, f, indent=2)
                self.status_bar.config(text=f"Exported to {file_path}")
                messagebox.showinfo("Success", f"Palette exported to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def export_css(self):
        """Export palette as CSS file"""
        if not self.custom_colors:
            messagebox.showwarning("No Colors", "Please add colors to the palette first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".css",
            filetypes=[("CSS files", "*.css"), ("All files", "*.*")],
            initialfile="color_palette.css"
        )

        if file_path:
            css_content = "/* Color Palette CSS Variables */\n"
            css_content += ":root {\n"

            for i, color in enumerate(self.custom_colors, 1):
                css_content += f"    --color-{i}: {color};\n"

            css_content += "}\n\n"
            css_content += "/* Color Classes */\n"

            for i, color in enumerate(self.custom_colors, 1):
                css_content += f".color-{i} {{\n"
                css_content += f"    color: {color};\n"
                css_content += "}\n\n"

                css_content += f".bg-color-{i} {{\n"
                css_content += f"    background-color: {color};\n"
                css_content += "}\n\n"

            try:
                with open(file_path, 'w') as f:
                    f.write(css_content)
                self.status_bar.config(text=f"Exported to {file_path}")
                messagebox.showinfo("Success", f"CSS exported to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def export_image(self):
        """Export palette as PNG image"""
        if not self.custom_colors:
            messagebox.showwarning("No Colors", "Please add colors to the palette first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
            initialfile="color_palette.png"
        )

        if file_path:
            try:
                # Create image
                width = 800
                height = 400
                img = Image.new('RGB', (width, height), 'white')
                draw = ImageDraw.Draw(img)

                # Draw title
                from PIL import ImageFont
                try:
                    font = ImageFont.truetype("arial.ttf", 24)
                except:
                    font = ImageFont.load_default()

                draw.text((20, 20), "Color Palette", fill='black', font=font)

                # Draw color swatches
                num_colors = len(self.custom_colors)
                swatch_width = width // num_colors

                for i, color in enumerate(self.custom_colors):
                    x1 = i * swatch_width
                    x2 = x1 + swatch_width
                    y1 = 100
                    y2 = 300

                    # Convert hex to RGB tuple
                    if color.startswith("#"):
                        r = int(color[1:3], 16)
                        g = int(color[3:5], 16)
                        b = int(color[5:7], 16)
                        rgb = (r, g, b)
                    else:
                        rgb = (0, 0, 0)

                    # Draw color rectangle
                    draw.rectangle([x1, y1, x2, y2], fill=rgb, outline='black')

                    # Draw color code
                    draw.text((x1 + 10, y2 + 20), color, fill='black', font=font)

                # Save image
                img.save(file_path)
                self.status_bar.config(text=f"Exported to {file_path}")
                messagebox.showinfo("Success", f"Image exported to:\n{file_path}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to export image: {str(e)}")


def main():
    root = tk.Tk()
    app = ColorPaletteApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()