import sys
import colorsys
import random
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
import pyperclip


class ColorPickerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_color = QtGui.QColor(255, 0, 0)
        self.saved_colors = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Color Picker & Palette Generator')
        self.setGeometry(100, 100, 1200, 700)

        # Create menu bar
        self.create_menu_bar()

        # Create main layout
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QtWidgets.QHBoxLayout(main_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Left panel - Color Picker
        left_panel = self.create_color_picker_panel()
        main_layout.addWidget(left_panel)

        # Center panel - Sliders
        center_panel = self.create_sliders_panel()
        main_layout.addWidget(center_panel)

        # Right panel - Palette Generator
        right_panel = self.create_palette_panel()
        main_layout.addWidget(right_panel)

        # Status bar
        self.statusBar().showMessage('Ready | Click on palette colors to select them')

        # Initial update
        self.update_color(self.current_color)

    def create_menu_bar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')

        export_action = QtWidgets.QAction('Export Palette as CSS', self)
        export_action.triggered.connect(self.export_palette)
        file_menu.addAction(export_action)

        clear_action = QtWidgets.QAction('Clear Saved Colors', self)
        clear_action.triggered.connect(self.clear_saved_colors)
        file_menu.addAction(clear_action)

        file_menu.addSeparator()

        exit_action = QtWidgets.QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Tools menu
        tools_menu = menubar.addMenu('Tools')

        random_action = QtWidgets.QAction('Random Color', self)
        random_action.triggered.connect(self.generate_random_color)
        tools_menu.addAction(random_action)

        complementary_action = QtWidgets.QAction('Generate Complementary', self)
        complementary_action.triggered.connect(lambda: self.generate_palette('Complementary'))
        tools_menu.addAction(complementary_action)

        tools_menu.addSeparator()

        mixer_action = QtWidgets.QAction('Color Mixer', self)
        mixer_action.triggered.connect(self.open_color_mixer)
        tools_menu.addAction(mixer_action)

        library_action = QtWidgets.QAction('Color Library', self)
        library_action.triggered.connect(self.open_color_library)
        tools_menu.addAction(library_action)

        # Help menu
        help_menu = menubar.addMenu('Help')

        about_action = QtWidgets.QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_color_picker_panel(self):
        panel = QtWidgets.QFrame()
        panel.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        panel.setFixedWidth(320)

        layout = QtWidgets.QVBoxLayout(panel)
        layout.setSpacing(15)

        # Title
        title = QtWidgets.QLabel('Color Picker')
        title.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout.addWidget(title)

        # Color preview
        self.color_preview = QtWidgets.QLabel()
        self.color_preview.setFixedSize(280, 200)
        self.color_preview.setStyleSheet('background-color: red; border-radius: 10px;')
        layout.addWidget(self.color_preview, alignment=Qt.AlignCenter)

        # Color picker button
        self.color_picker_btn = QtWidgets.QPushButton('Pick Color')
        self.color_picker_btn.clicked.connect(self.open_color_dialog)
        self.color_picker_btn.setFixedSize(280, 30)
        layout.addWidget(self.color_picker_btn, alignment=Qt.AlignCenter)

        # Color values display
        values_group = QtWidgets.QGroupBox('Color Values')
        values_layout = QtWidgets.QVBoxLayout(values_group)

        # HEX
        hex_layout = QtWidgets.QHBoxLayout()
        hex_label = QtWidgets.QLabel('HEX:')
        hex_label.setFixedWidth(50)
        self.hex_field = QtWidgets.QLineEdit('#FF0000')
        self.hex_field.setReadOnly(True)
        copy_hex_btn = QtWidgets.QPushButton('Copy')
        copy_hex_btn.clicked.connect(lambda: self.copy_to_clipboard(self.hex_field.text()))
        hex_layout.addWidget(hex_label)
        hex_layout.addWidget(self.hex_field)
        hex_layout.addWidget(copy_hex_btn)
        values_layout.addLayout(hex_layout)

        # RGB
        rgb_layout = QtWidgets.QHBoxLayout()
        rgb_label = QtWidgets.QLabel('RGB:')
        rgb_label.setFixedWidth(50)
        self.rgb_field = QtWidgets.QLineEdit('rgb(255, 0, 0)')
        self.rgb_field.setReadOnly(True)
        copy_rgb_btn = QtWidgets.QPushButton('Copy')
        copy_rgb_btn.clicked.connect(lambda: self.copy_to_clipboard(self.rgb_field.text()))
        rgb_layout.addWidget(rgb_label)
        rgb_layout.addWidget(self.rgb_field)
        rgb_layout.addWidget(copy_rgb_btn)
        values_layout.addLayout(rgb_layout)

        # HSL
        hsl_layout = QtWidgets.QHBoxLayout()
        hsl_label = QtWidgets.QLabel('HSL:')
        hsl_label.setFixedWidth(50)
        self.hsl_field = QtWidgets.QLineEdit('hsl(0, 100%, 50%)')
        self.hsl_field.setReadOnly(True)
        copy_hsl_btn = QtWidgets.QPushButton('Copy')
        copy_hsl_btn.clicked.connect(lambda: self.copy_to_clipboard(self.hsl_field.text()))
        hsl_layout.addWidget(hsl_label)
        hsl_layout.addWidget(self.hsl_field)
        hsl_layout.addWidget(copy_hsl_btn)
        values_layout.addLayout(hsl_layout)

        layout.addWidget(values_group)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()

        save_btn = QtWidgets.QPushButton('Save Color')
        save_btn.setStyleSheet('background-color: #27ae60; color: white;')
        save_btn.clicked.connect(self.save_current_color)

        random_btn = QtWidgets.QPushButton('Random')
        random_btn.setStyleSheet('background-color: #3498db; color: white;')
        random_btn.clicked.connect(self.generate_random_color)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(random_btn)
        layout.addLayout(button_layout)

        # Color mixer button
        mixer_btn = QtWidgets.QPushButton('Color Mixer')
        mixer_btn.setStyleSheet('background-color: #e67e22; color: white;')
        mixer_btn.clicked.connect(self.open_color_mixer)
        layout.addWidget(mixer_btn)

        return panel

    def create_sliders_panel(self):
        panel = QtWidgets.QFrame()
        panel.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        panel.setFixedWidth(300)

        layout = QtWidgets.QVBoxLayout(panel)
        layout.setSpacing(15)

        # Title
        title = QtWidgets.QLabel('Adjust Colors')
        title.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout.addWidget(title)

        # RGB Sliders
        rgb_group = QtWidgets.QGroupBox('RGB Values')
        rgb_layout = QtWidgets.QVBoxLayout(rgb_group)

        # Red slider
        self.red_label = QtWidgets.QLabel('Red: 255')
        self.red_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.red_slider.setRange(0, 255)
        self.red_slider.setValue(255)
        self.red_slider.valueChanged.connect(self.update_from_rgb)
        rgb_layout.addWidget(self.red_label)
        rgb_layout.addWidget(self.red_slider)

        # Green slider
        self.green_label = QtWidgets.QLabel('Green: 0')
        self.green_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.green_slider.setRange(0, 255)
        self.green_slider.setValue(0)
        self.green_slider.valueChanged.connect(self.update_from_rgb)
        rgb_layout.addWidget(self.green_label)
        rgb_layout.addWidget(self.green_slider)

        # Blue slider
        self.blue_label = QtWidgets.QLabel('Blue: 0')
        self.blue_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.blue_slider.setRange(0, 255)
        self.blue_slider.setValue(0)
        self.blue_slider.valueChanged.connect(self.update_from_rgb)
        rgb_layout.addWidget(self.blue_label)
        rgb_layout.addWidget(self.blue_slider)

        layout.addWidget(rgb_group)

        # HSL Sliders
        hsl_group = QtWidgets.QGroupBox('HSL Values')
        hsl_layout = QtWidgets.QVBoxLayout(hsl_group)

        # Hue slider
        self.hue_label = QtWidgets.QLabel('Hue: 0')
        self.hue_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.hue_slider.setRange(0, 360)
        self.hue_slider.setValue(0)
        self.hue_slider.valueChanged.connect(self.update_from_hsl)
        hsl_layout.addWidget(self.hue_label)
        hsl_layout.addWidget(self.hue_slider)

        # Saturation slider
        self.sat_label = QtWidgets.QLabel('Saturation: 100%')
        self.sat_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.sat_slider.setRange(0, 100)
        self.sat_slider.setValue(100)
        self.sat_slider.valueChanged.connect(self.update_from_hsl)
        hsl_layout.addWidget(self.sat_label)
        hsl_layout.addWidget(self.sat_slider)

        # Lightness slider
        self.light_label = QtWidgets.QLabel('Lightness: 50%')
        self.light_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.light_slider.setRange(0, 100)
        self.light_slider.setValue(50)
        self.light_slider.valueChanged.connect(self.update_from_hsl)
        hsl_layout.addWidget(self.light_label)
        hsl_layout.addWidget(self.light_slider)

        layout.addWidget(hsl_group)

        return panel

    def create_palette_panel(self):
        panel = QtWidgets.QFrame()
        panel.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        panel.setFixedWidth(350)

        layout = QtWidgets.QVBoxLayout(panel)
        layout.setSpacing(15)

        # Title
        title = QtWidgets.QLabel('Palette Generator')
        title.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout.addWidget(title)

        # Harmony mode selection
        harmony_layout = QtWidgets.QHBoxLayout()
        harmony_label = QtWidgets.QLabel('Harmony:')
        self.harmony_combo = QtWidgets.QComboBox()
        self.harmony_combo.addItems([
            'Complementary',
            'Analogous',
            'Triadic',
            'Split Complementary',
            'Tetradic',
            'Monochromatic',
            'Random Palette'
        ])
        self.harmony_combo.currentTextChanged.connect(self.generate_palette)
        harmony_layout.addWidget(harmony_label)
        harmony_layout.addWidget(self.harmony_combo)
        layout.addLayout(harmony_layout)

        # Generate button
        generate_btn = QtWidgets.QPushButton('Generate Palette')
        generate_btn.setStyleSheet('background-color: #9b59b6; color: white;')
        generate_btn.clicked.connect(lambda: self.generate_palette())
        layout.addWidget(generate_btn)

        # Generated palette
        palette_label = QtWidgets.QLabel('Generated Palette:')
        palette_label.setStyleSheet('font-weight: bold;')
        layout.addWidget(palette_label)

        self.palette_container = QtWidgets.QScrollArea()
        self.palette_container.setWidgetResizable(True)
        self.palette_widget = QtWidgets.QWidget()
        self.palette_layout = QtWidgets.QGridLayout(self.palette_widget)
        self.palette_container.setWidget(self.palette_widget)
        self.palette_container.setFixedHeight(150)
        layout.addWidget(self.palette_container)

        # Saved colors
        saved_label = QtWidgets.QLabel('Saved Colors:')
        saved_label.setStyleSheet('font-weight: bold;')
        layout.addWidget(saved_label)

        self.saved_colors_container = QtWidgets.QScrollArea()
        self.saved_colors_container.setWidgetResizable(True)
        self.saved_colors_widget = QtWidgets.QWidget()
        self.saved_colors_layout = QtWidgets.QGridLayout(self.saved_colors_widget)
        self.saved_colors_container.setWidget(self.saved_colors_widget)
        self.saved_colors_container.setFixedHeight(100)
        layout.addWidget(self.saved_colors_container)

        # Clear saved button
        clear_btn = QtWidgets.QPushButton('Clear Saved')
        clear_btn.setStyleSheet('background-color: #e74c3c; color: white;')
        clear_btn.clicked.connect(self.clear_saved_colors)
        layout.addWidget(clear_btn)

        return panel

    def open_color_dialog(self):
        color = QtWidgets.QColorDialog.getColor(self.current_color, self, 'Select Color')
        if color.isValid():
            self.update_color(color)

    def update_color(self, color):
        self.current_color = color

        # Update preview
        self.color_preview.setStyleSheet(f'background-color: {color.name()}; border-radius: 10px;')

        # Update color values
        self.hex_field.setText(color.name())
        self.rgb_field.setText(f'rgb({color.red()}, {color.green()}, {color.blue()})')

        # Convert to HSL
        h, s, l = self.rgb_to_hsl(color.red(), color.green(), color.blue())
        self.hsl_field.setText(f'hsl({int(h)}, {int(s)}%, {int(l)}%)')

        # Update RGB sliders
        self.red_slider.setValue(color.red())
        self.green_slider.setValue(color.green())
        self.blue_slider.setValue(color.blue())
        self.red_label.setText(f'Red: {color.red()}')
        self.green_label.setText(f'Green: {color.green()}')
        self.blue_label.setText(f'Blue: {color.blue()}')

        # Update HSL sliders
        self.hue_slider.setValue(int(h))
        self.sat_slider.setValue(int(s))
        self.light_slider.setValue(int(l))
        self.hue_label.setText(f'Hue: {int(h)}')
        self.sat_label.setText(f'Saturation: {int(s)}%')
        self.light_label.setText(f'Lightness: {int(l)}%')

        # Generate palette
        self.generate_palette()

    def update_from_rgb(self):
        color = QtGui.QColor(
            self.red_slider.value(),
            self.green_slider.value(),
            self.blue_slider.value()
        )
        self.update_color(color)

    def update_from_hsl(self):
        h = self.hue_slider.value()
        s = self.sat_slider.value() / 100.0
        l = self.light_slider.value() / 100.0

        # Convert HSL to RGB
        r, g, b = self.hsl_to_rgb(h, s, l)
        color = QtGui.QColor(int(r * 255), int(g * 255), int(b * 255))
        self.update_color(color)

    def generate_palette(self, harmony_type=None):
        if harmony_type is None:
            harmony_type = self.harmony_combo.currentText()

        # Clear current palette
        for i in reversed(range(self.palette_layout.count())):
            widget = self.palette_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        colors = []

        if harmony_type == 'Complementary':
            colors = self.generate_complementary()
        elif harmony_type == 'Analogous':
            colors = self.generate_analogous()
        elif harmony_type == 'Triadic':
            colors = self.generate_triadic()
        elif harmony_type == 'Split Complementary':
            colors = self.generate_split_complementary()
        elif harmony_type == 'Tetradic':
            colors = self.generate_tetradic()
        elif harmony_type == 'Monochromatic':
            colors = self.generate_monochromatic()
        elif harmony_type == 'Random Palette':
            colors = self.generate_random_palette()

        # Display palette
        for i, color in enumerate(colors):
            self.add_color_to_palette(color, self.palette_layout, i)

    def generate_complementary(self):
        h, s, l = self.rgb_to_hsl(
            self.current_color.red(),
            self.current_color.green(),
            self.current_color.blue()
        )
        h2 = (h + 180) % 360
        r2, g2, b2 = self.hsl_to_rgb(h2, s / 100.0, l / 100.0)

        return [
            self.current_color,
            QtGui.QColor(int(r2 * 255), int(g2 * 255), int(b2 * 255))
        ]

    def generate_analogous(self):
        h, s, l = self.rgb_to_hsl(
            self.current_color.red(),
            self.current_color.green(),
            self.current_color.blue()
        )

        colors = []
        for offset in [-30, 0, 30]:
            h2 = (h + offset) % 360
            r2, g2, b2 = self.hsl_to_rgb(h2, s / 100.0, l / 100.0)
            colors.append(QtGui.QColor(int(r2 * 255), int(g2 * 255), int(b2 * 255)))

        return colors

    def generate_triadic(self):
        h, s, l = self.rgb_to_hsl(
            self.current_color.red(),
            self.current_color.green(),
            self.current_color.blue()
        )

        colors = [self.current_color]
        for offset in [120, 240]:
            h2 = (h + offset) % 360
            r2, g2, b2 = self.hsl_to_rgb(h2, s / 100.0, l / 100.0)
            colors.append(QtGui.QColor(int(r2 * 255), int(g2 * 255), int(b2 * 255)))

        return colors

    def generate_split_complementary(self):
        h, s, l = self.rgb_to_hsl(
            self.current_color.red(),
            self.current_color.green(),
            self.current_color.blue()
        )

        colors = [self.current_color]
        for offset in [150, 210]:
            h2 = (h + offset) % 360
            r2, g2, b2 = self.hsl_to_rgb(h2, s / 100.0, l / 100.0)
            colors.append(QtGui.QColor(int(r2 * 255), int(g2 * 255), int(b2 * 255)))

        return colors

    def generate_tetradic(self):
        h, s, l = self.rgb_to_hsl(
            self.current_color.red(),
            self.current_color.green(),
            self.current_color.blue()
        )

        colors = [self.current_color]
        for offset in [90, 180, 270]:
            h2 = (h + offset) % 360
            r2, g2, b2 = self.hsl_to_rgb(h2, s / 100.0, l / 100.0)
            colors.append(QtGui.QColor(int(r2 * 255), int(g2 * 255), int(b2 * 255)))

        return colors

    def generate_monochromatic(self):
        h, s, l = self.rgb_to_hsl(
            self.current_color.red(),
            self.current_color.green(),
            self.current_color.blue()
        )

        colors = []
        for lightness in [0.3, 0.5, 0.7, 0.9]:
            r2, g2, b2 = self.hsl_to_rgb(h, s / 100.0, lightness)
            colors.append(QtGui.QColor(int(r2 * 255), int(g2 * 255), int(b2 * 255)))

        return colors

    def generate_random_palette(self):
        colors = []
        for _ in range(5):
            color = QtGui.QColor(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            colors.append(color)
        return colors

    def add_color_to_palette(self, color, layout, index):
        color_widget = QtWidgets.QWidget()
        color_layout = QtWidgets.QVBoxLayout(color_widget)

        # Color square
        color_box = QtWidgets.QLabel()
        color_box.setFixedSize(60, 60)
        color_box.setStyleSheet(f'background-color: {color.name()}; border-radius: 5px;')
        color_box.setCursor(Qt.PointingHandCursor)
        color_box.mousePressEvent = lambda e: self.update_color(color)

        # HEX label
        hex_label = QtWidgets.QLabel(color.name())
        hex_label.setStyleSheet('font-family: monospace; font-size: 10px;')
        hex_label.setAlignment(Qt.AlignCenter)

        color_layout.addWidget(color_box, alignment=Qt.AlignCenter)
        color_layout.addWidget(hex_label, alignment=Qt.AlignCenter)

        # Add to layout
        row = index // 4
        col = index % 4
        layout.addWidget(color_widget, row, col)

    def save_current_color(self):
        if self.current_color not in self.saved_colors:
            self.saved_colors.append(self.current_color)
            self.add_color_to_palette(
                self.current_color,
                self.saved_colors_layout,
                len(self.saved_colors) - 1
            )

    def clear_saved_colors(self):
        self.saved_colors = []
        for i in reversed(range(self.saved_colors_layout.count())):
            widget = self.saved_colors_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def generate_random_color(self):
        color = QtGui.QColor(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        self.update_color(color)

    def export_palette(self):
        css = "/* Generated Color Palette */\n\n"
        css += "/* Current Color */\n"
        css += ":root {\n"
        css += f"  --current-color: {self.current_color.name()};\n"
        css += "}\n\n"

        if self.saved_colors:
            css += "/* Saved Colors */\n"
            for i, color in enumerate(self.saved_colors):
                css += f"  --color-{i + 1}: {color.name()};\n"

        # Display CSS
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Export CSS")
        dialog.setFixedSize(500, 300)

        layout = QtWidgets.QVBoxLayout(dialog)

        text_edit = QtWidgets.QTextEdit()
        text_edit.setPlainText(css)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)

        dialog.exec_()

    def open_color_mixer(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Color Mixer")
        dialog.setFixedSize(500, 400)

        layout = QtWidgets.QVBoxLayout(dialog)

        # Color 1
        color1_layout = QtWidgets.QHBoxLayout()
        color1_label = QtWidgets.QLabel("Color 1:")
        self.mixer_color1 = QtWidgets.QLineEdit(self.current_color.name())
        self.mixer_color1_btn = QtWidgets.QPushButton("Pick")
        self.mixer_color1_btn.clicked.connect(lambda: self.pick_mixer_color(1))
        color1_layout.addWidget(color1_label)
        color1_layout.addWidget(self.mixer_color1)
        color1_layout.addWidget(self.mixer_color1_btn)
        layout.addLayout(color1_layout)

        # Color 2
        color2_layout = QtWidgets.QHBoxLayout()
        color2_label = QtWidgets.QLabel("Color 2:")
        self.mixer_color2 = QtWidgets.QLineEdit("#0000FF")
        self.mixer_color2_btn = QtWidgets.QPushButton("Pick")
        self.mixer_color2_btn.clicked.connect(lambda: self.pick_mixer_color(2))
        color2_layout.addWidget(color2_label)
        color2_layout.addWidget(self.mixer_color2)
        color2_layout.addWidget(self.mixer_color2_btn)
        layout.addLayout(color2_layout)

        # Blend mode selection
        blend_layout = QtWidgets.QHBoxLayout()
        blend_label = QtWidgets.QLabel("Blend Mode:")
        self.blend_combo = QtWidgets.QComboBox()
        self.blend_combo.addItems(["Average", "Additive"])
        blend_layout.addWidget(blend_label)
        blend_layout.addWidget(self.blend_combo)
        layout.addLayout(blend_layout)

        # Mix button
        mix_btn = QtWidgets.QPushButton("Mix Colors")
        mix_btn.clicked.connect(self.mix_colors)
        layout.addWidget(mix_btn)

        # Result display
        self.mixer_result = QtWidgets.QLabel()
        self.mixer_result.setFixedSize(100, 100)
        self.mixer_result.setStyleSheet("background-color: gray; border-radius: 5px;")
        layout.addWidget(self.mixer_result, alignment=Qt.AlignCenter)

        self.mixer_result_text = QtWidgets.QLineEdit()
        self.mixer_result_text.setReadOnly(True)
        layout.addWidget(self.mixer_result_text)

        copy_btn = QtWidgets.QPushButton("Copy Result")
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(self.mixer_result_text.text()))
        layout.addWidget(copy_btn)

        dialog.exec_()

    def pick_mixer_color(self, num):
        color = QtWidgets.QColorDialog.getColor(self.current_color, self, 'Select Color')
        if color.isValid():
            if num == 1:
                self.mixer_color1.setText(color.name())
            else:
                self.mixer_color2.setText(color.name())

    def mix_colors(self):
        try:
            color1 = QtGui.QColor(self.mixer_color1.text())
            color2 = QtGui.QColor(self.mixer_color2.text())

            if not color1.isValid() or not color2.isValid():
                QtWidgets.QMessageBox.warning(self, "Error", "Invalid color format")
                return

            blend_mode = self.blend_combo.currentText()

            if blend_mode == "Average":
                # Average blending
                r = (color1.red() + color2.red()) // 2
                g = (color1.green() + color2.green()) // 2
                b = (color1.blue() + color2.blue()) // 2
            else:  # Additive
                # Additive blending (capped at 255)
                r = min(color1.red() + color2.red(), 255)
                g = min(color1.green() + color2.green(), 255)
                b = min(color1.blue() + color2.blue(), 255)

            result = QtGui.QColor(r, g, b)
            self.mixer_result.setStyleSheet(f"background-color: {result.name()}; border-radius: 5px;")
            self.mixer_result_text.setText(result.name())

        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Could not mix colors: {str(e)}")

    def open_color_library(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Color Library")
        dialog.setFixedSize(600, 500)

        layout = QtWidgets.QVBoxLayout(dialog)

        # Search box
        search_layout = QtWidgets.QHBoxLayout()
        search_label = QtWidgets.QLabel("Search:")
        search_input = QtWidgets.QLineEdit()
        search_input.setPlaceholderText("Type color name...")
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_input)
        layout.addLayout(search_layout)

        # Color list
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        color_widget = QtWidgets.QWidget()
        color_layout = QtWidgets.QVBoxLayout(color_widget)

        # Color data
        color_data = [
            ("AliceBlue", "#F0F8FF"), ("AntiqueWhite", "#FAEBD7"), ("Aqua", "#00FFFF"), ("Aquamarine", "#7FFFD4"),
            ("Azure", "#F0FFFF"), ("Beige", "#F5F5DC"), ("Bisque", "#FFE4C4"), ("Black", "#000000"),
            ("BlanchedAlmond", "#FFEBCD"), ("Blue", "#0000FF"), ("BlueViolet", "#8A2BE2"), ("Brown", "#A52A2A"),
            ("BurlyWood", "#DEB887"), ("CadetBlue", "#5F9EA0"), ("Chartreuse", "#7FFF00"), ("Chocolate", "#D2691E"),
            ("Coral", "#FF7F50"), ("CornflowerBlue", "#6495ED"), ("Cornsilk", "#FFF8DC"), ("Crimson", "#DC143C"),
            ("Cyan", "#00FFFF"), ("DarkBlue", "#00008B"), ("DarkCyan", "#008B8B"), ("DarkGoldenRod", "#B8860B"),
            ("DarkGray", "#A9A9A9"), ("DarkGreen", "#006400"), ("DarkKhaki", "#BDB76B"), ("DarkMagenta", "#8B008B"),
            ("DarkOliveGreen", "#556B2F"), ("DarkOrange", "#FF8C00"), ("DarkOrchid", "#9932CC"), ("DarkRed", "#8B0000"),
            ("DarkSalmon", "#E9967A"), ("DarkSeaGreen", "#8FBC8F"), ("DarkSlateBlue", "#483D8B"),
            ("DarkSlateGray", "#2F4F4F"),
            ("DarkTurquoise", "#00CED1"), ("DarkViolet", "#9400D3"), ("DeepPink", "#FF1493"),
            ("DeepSkyBlue", "#00BFFF"),
            ("DimGray", "#696969"), ("DodgerBlue", "#1E90FF"), ("FireBrick", "#B22222"), ("FloralWhite", "#FFFAF0"),
            ("ForestGreen", "#228B22"), ("Fuchsia", "#FF00FF"), ("Gainsboro", "#DCDCDC"), ("GhostWhite", "#F8F8FF"),
            ("Gold", "#FFD700"), ("GoldenRod", "#DAA520"), ("Gray", "#808080"), ("Green", "#008000"),
            ("GreenYellow", "#ADFF2F"), ("HoneyDew", "#F0FFF0"), ("HotPink", "#FF69B4"), ("IndianRed", "#CD5C5C"),
            ("Indigo", "#4B0082"), ("Ivory", "#FFFFF0"), ("Khaki", "#F0E68C"), ("Lavender", "#E6E6FA"),
            ("LavenderBlush", "#FFF0F5"), ("LawnGreen", "#7CFC00"), ("LemonChiffon", "#FFFACD"),
            ("LightBlue", "#ADD8E6"),
            ("LightCoral", "#F08080"), ("LightCyan", "#E0FFFF"), ("LightGoldenRodYellow", "#FAFAD2"),
            ("LightGray", "#D3D3D3"),
            ("LightGreen", "#90EE90"), ("LightPink", "#FFB6C1"), ("LightSalmon", "#FFA07A"),
            ("LightSeaGreen", "#20B2AA"),
            ("LightSkyBlue", "#87CEFA"), ("LightSlateGray", "#778899"), ("LightSteelBlue", "#B0C4DE"),
            ("LightYellow", "#FFFFE0"),
            ("Lime", "#00FF00"), ("LimeGreen", "#32CD32"), ("Linen", "#FAF0E6"), ("Magenta", "#FF00FF"),
            ("Maroon", "#800000"), ("MediumAquaMarine", "#66CDAA"), ("MediumBlue", "#0000CD"),
            ("MediumOrchid", "#BA55D3"),
            ("MediumPurple", "#9370DB"), ("MediumSeaGreen", "#3CB371"), ("MediumSlateBlue", "#7B68EE"),
            ("MediumSpringGreen", "#00FA9A"),
            ("MediumTurquoise", "#48D1CC"), ("MediumVioletRed", "#C71585"), ("MidnightBlue", "#191970"),
            ("MintCream", "#F5FFFA"),
            ("MistyRose", "#FFE4E1"), ("Moccasin", "#FFE4B5"), ("NavajoWhite", "#FFDEAD"), ("Navy", "#000080"),
            ("OldLace", "#FDF5E6"), ("Olive", "#808000"), ("OliveDrab", "#6B8E23"), ("Orange", "#FFA500"),
            ("OrangeRed", "#FF4500"), ("Orchid", "#DA70D6"), ("PaleGoldenRod", "#EEE8AA"), ("PaleGreen", "#98FB98"),
            ("PaleTurquoise", "#AFEEEE"), ("PaleVioletRed", "#DB7093"), ("PapayaWhip", "#FFEFD5"),
            ("PeachPuff", "#FFDAB9"),
            ("Peru", "#CD853F"), ("Pink", "#FFC0CB"), ("Plum", "#DDA0DD"), ("PowderBlue", "#B0E0E6"),
            ("Purple", "#800080"), ("RebeccaPurple", "#663399"), ("Red", "#FF0000"), ("RosyBrown", "#BC8F8F"),
            ("RoyalBlue", "#4169E1"), ("SaddleBrown", "#8B4513"), ("Salmon", "#FA8072"), ("SandyBrown", "#F4A460"),
            ("SeaGreen", "#2E8B57"), ("SeaShell", "#FFF5EE"), ("Sienna", "#A0522D"), ("Silver", "#C0C0C0"),
            ("SkyBlue", "#87CEEB"), ("SlateBlue", "#6A5ACD"), ("SlateGray", "#708090"), ("Snow", "#FFFAFA"),
            ("SpringGreen", "#00FF7F"), ("SteelBlue", "#4682B4"), ("Tan", "#D2B48C"), ("Teal", "#008080"),
            ("Thistle", "#D8BFD8"), ("Tomato", "#FF6347"), ("Turquoise", "#40E0D0"), ("Violet", "#EE82EE"),
            ("Wheat", "#F5DEB3"), ("White", "#FFFFFF"), ("WhiteSmoke", "#F5F5F5"), ("Yellow", "#FFFF00"),
            ("YellowGreen", "#9ACD32")
        ]

        # Create color items
        for name, hex_code in color_data:
            item_widget = self.create_color_library_item(name, hex_code, dialog)
            color_layout.addWidget(item_widget)

        scroll.setWidget(color_widget)
        layout.addWidget(scroll)

        # Search functionality
        def filter_colors():
            search_text = search_input.text().lower()
            # Clear and rebuild with filtered items
            for i in reversed(range(color_layout.count())):
                widget = color_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            for name, hex_code in color_data:
                if search_text in name.lower() or search_text in hex_code.lower():
                    item_widget = self.create_color_library_item(name, hex_code, dialog)
                    color_layout.addWidget(item_widget)

        search_input.textChanged.connect(filter_colors)

        dialog.exec_()

    def create_color_library_item(self, name, hex_code, parent_dialog):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)

        # Color preview
        color_box = QtWidgets.QLabel()
        color_box.setFixedSize(40, 40)
        color_box.setStyleSheet(f"background-color: {hex_code}; border-radius: 5px;")

        # Color information
        info_layout = QtWidgets.QVBoxLayout()
        name_label = QtWidgets.QLabel(name)
        name_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        hex_label = QtWidgets.QLabel(hex_code)
        hex_label.setStyleSheet("font-family: monospace; color: gray; font-size: 10px;")
        info_layout.addWidget(name_label)
        info_layout.addWidget(hex_label)

        # Buttons
        select_btn = QtWidgets.QPushButton("Select")
        select_btn.setFixedSize(60, 25)
        select_btn.clicked.connect(lambda: self.select_library_color(hex_code, parent_dialog))

        copy_btn = QtWidgets.QPushButton("Copy")
        copy_btn.setFixedSize(60, 25)
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(hex_code))

        layout.addWidget(color_box)
        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addWidget(select_btn)
        layout.addWidget(copy_btn)

        return widget

    def select_library_color(self, hex_code, dialog):
        color = QtGui.QColor(hex_code)
        if color.isValid():
            self.update_color(color)
            dialog.close()

    def copy_to_clipboard(self, text):
        try:
            pyperclip.copy(text)
            self.statusBar().showMessage(f"Copied: {text}", 2000)
        except:
            # Fallback if pyperclip doesn't work
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(text)
            self.statusBar().showMessage(f"Copied: {text}", 2000)

    def show_about(self):
        QtWidgets.QMessageBox.about(self, "About Color Picker",
                                    "Color Picker & Palette Generator\n\n"
                                    "A comprehensive color tool for designers\n\n"
                                    "Features:\n"
                                    "✓ Pick any color\n"
                                    "✓ RGB & HSL sliders\n"
                                    "✓ HEX, RGB, HSL formats\n"
                                    "✓ Color harmony palettes\n"
                                    "✓ Save favorite colors\n"
                                    "✓ Export as CSS\n"
                                    "✓ Random color generator\n"
                                    "✓ Color Mixer\n"
                                    "✓ Color Library with 200+ colors\n\n"
                                    "Version: 1.0\n"
                                    "Created with PyQt5")

    def rgb_to_hsl(self, r, g, b):
        r = r / 255.0
        g = g / 255.0
        b = b / 255.0

        h, l, s = colorsys.rgb_to_hls(r, g, b)
        h = h * 360
        s = s * 100
        l = l * 100

        return h, s, l

    def hsl_to_rgb(self, h, s, l):
        h = h / 360.0
        rgb = colorsys.hls_to_rgb(h, l, s)
        return rgb


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    # Set application style
    app.setStyleSheet("""
        QMainWindow {
            background-color: #ecf0f1;
        }
        QFrame {
            background-color: white;
            border-radius: 10px;
            padding: 15px;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        QPushButton {
            padding: 5px 10px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #f0f0f0;
        }
    """)

    window = ColorPickerApp()
    window.show()
    sys.exit(app.exec_())