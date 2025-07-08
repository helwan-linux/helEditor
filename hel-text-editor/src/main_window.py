import os
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QAction,
    QMenuBar, QTextEdit, QToolBar, QStatusBar, QComboBox
)
from PyQt5.QtGui import QIcon, QPixmap, QFontDatabase
from PyQt5.QtCore import Qt, QSize

# استيراد الكلاسات والدوال من ملفاتنا الجديدة
from .dialogs import FindDialog, FindReplaceDialog
from . import handlers # استيراد كل الدوال في handlers.py
# . يعني من نفس الـ package (src)

# المسار الأساسي للمشروع للوصول إلى الأيقونات
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Helwan Text Editor")
        self.setGeometry(100, 100, 900, 700)

        # تعديل المسار الصحيح للأيقونة
        icon_path = os.path.join(BASE_DIR, "assets", "images", "splash_screen.png")
        if os.path.exists(icon_path) and not QPixmap(icon_path).isNull():
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Warning: Application icon not found or invalid at: {icon_path}. Using default.")
            self.setWindowIcon(QIcon(QPixmap(1, 1).scaledToWidth(1, Qt.SmoothTransformation)))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.text_editor = QTextEdit()
        self.text_editor.setPlaceholderText("Start typing here...")
        self.text_editor.setLayoutDirection(Qt.LeftToRight)
        self.text_editor.setAlignment(Qt.AlignLeft)
        self.text_editor.setLineWrapMode(QTextEdit.WidgetWidth)
        self.text_editor.textChanged.connect(self.update_word_char_count)
        self.text_editor.cursorPositionChanged.connect(self.update_font_info_combos)
        main_layout.addWidget(self.text_editor)

        self.create_menu_bar()
        self.create_tool_bar()
        self.create_status_bar()

        self.update_word_char_count()
        self.update_font_info_combos()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        # --- قائمة File ---
        file_menu = menu_bar.addMenu("File")

        self.new_action = QAction("New", self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.setStatusTip("Create a new file")
        self.new_action.triggered.connect(lambda: handlers.new_file(self)) # ربط الدالة الجديدة
        file_menu.addAction(self.new_action)

        self.open_action = QAction("Open...", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.setStatusTip("Open an existing file")
        self.open_action.triggered.connect(lambda: handlers.open_file(self)) # ربط الدالة الجديدة
        file_menu.addAction(self.open_action)

        self.save_action = QAction("Save", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.setStatusTip("Save the current file")
        self.save_action.triggered.connect(lambda: handlers.save_file(self)) # ربط الدالة الجديدة
        file_menu.addAction(self.save_action)

        self.save_as_action = QAction("Save As...", self)
        self.save_as_action.setShortcut("Ctrl+Shift+S")
        self.save_as_action.setStatusTip("Save the current file with a new name")
        file_menu.addAction(self.save_as_action)
        self.save_as_action.triggered.connect(lambda: handlers.save_file_as(self)) # ربط الدالة الجديدة

        file_menu.addSeparator()

        self.cut_action = QAction("Cut", self)
        self.cut_action.setShortcut("Ctrl+X")
        self.cut_action.setStatusTip("Cut selected text")
        self.cut_action.triggered.connect(self.text_editor.cut)
        file_menu.addAction(self.cut_action)

        self.copy_action = QAction("Copy", self)
        self.copy_action.setShortcut("Ctrl+C")
        self.copy_action.setStatusTip("Copy selected text")
        self.copy_action.triggered.connect(self.text_editor.copy)
        file_menu.addAction(self.copy_action)

        self.paste_action = QAction("Paste", self)
        self.paste_action.setShortcut("Ctrl+V")
        self.paste_action.setStatusTip("Paste text from clipboard")
        self.paste_action.triggered.connect(self.text_editor.paste)
        file_menu.addAction(self.paste_action)

        file_menu.addSeparator()

        self.select_all_action = QAction("Select All", self)
        self.select_all_action.setShortcut("Ctrl+A")
        self.select_all_action.setStatusTip("Select all text in the document")
        self.select_all_action.triggered.connect(self.text_editor.selectAll)
        file_menu.addAction(self.select_all_action)

        file_menu.addSeparator()

        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.setStatusTip("Exit the application")
        self.exit_action.triggered.connect(self.close)
        file_menu.addAction(self.exit_action)

        # --- قائمة Edit (للتراجع والإعادة والبحث والاستبدال) ---
        edit_menu = menu_bar.addMenu("Edit")

        self.undo_action = QAction("Undo", self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.setStatusTip("Undo the last action")
        self.undo_action.triggered.connect(self.text_editor.undo)
        edit_menu.addAction(self.undo_action)

        self.redo_action = QAction("Redo", self)
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.setStatusTip("Redo the last undone action")
        self.redo_action.triggered.connect(self.text_editor.redo)
        edit_menu.addAction(self.redo_action)

        edit_menu.addSeparator()

        self.find_action = QAction("Find...", self)
        self.find_action.setShortcut("Ctrl+F")
        self.find_action.setStatusTip("Find text in the document")
        self.find_action.triggered.connect(self.show_find_dialog) # ما زالت دالة داخل MainWindow
        edit_menu.addAction(self.find_action)

        self.replace_action = QAction("Replace...", self)
        self.replace_action.setShortcut("Ctrl+H")
        self.replace_action.setStatusTip("Find and replace text in the document")
        self.replace_action.triggered.connect(self.show_find_replace_dialog) # ما زالت دالة داخل MainWindow
        edit_menu.addAction(self.replace_action)

        # --- قائمة Format ---
        format_menu = menu_bar.addMenu("Format")

        self.bold_action = QAction("Bold", self)
        self.bold_action.setShortcut("Ctrl+B")
        self.bold_action.setStatusTip("Make selected text bold")
        self.bold_action.triggered.connect(lambda: handlers.set_bold(self)) # ربط الدالة الجديدة
        format_menu.addAction(self.bold_action)

        self.italic_action = QAction("Italic", self)
        self.italic_action.setShortcut("Ctrl+I")
        self.italic_action.setStatusTip("Make selected text italic")
        self.italic_action.triggered.connect(lambda: handlers.set_italic(self)) # ربط الدالة الجديدة
        format_menu.addAction(self.italic_action)

        self.underline_action = QAction("Underline", self)
        self.underline_action.setShortcut("Ctrl+U")
        self.underline_action.setStatusTip("Underline selected text")
        self.underline_action.triggered.connect(lambda: handlers.set_underline(self)) # ربط الدالة الجديدة
        format_menu.addAction(self.underline_action)

        format_menu.addSeparator()

        self.font_color_action = QAction("Font Color...", self)
        self.font_color_action.setStatusTip("Change text color")
        self.font_color_action.triggered.connect(lambda: handlers.set_font_color(self)) # ربط الدالة الجديدة
        format_menu.addAction(self.font_color_action)

        self.bg_color_action = QAction("Highlight Color...", self)
        self.bg_color_action.setStatusTip("Change text background color (highlight)")
        self.bg_color_action.triggered.connect(lambda: handlers.set_text_background_color(self)) # ربط الدالة الجديدة
        format_menu.addAction(self.bg_color_action)

        format_menu.addSeparator()

        alignment_menu = format_menu.addMenu("Alignment")
        self.align_left_action = QAction("Align Left", self)
        self.align_left_action.setShortcut("Ctrl+L")
        self.align_left_action.setStatusTip("Align text to the left")
        self.align_left_action.triggered.connect(lambda: handlers.set_align_left(self)) # ربط الدالة الجديدة
        alignment_menu.addAction(self.align_left_action)

        self.align_center_action = QAction("Align Center", self)
        self.align_center_action.setShortcut("Ctrl+E")
        self.align_center_action.setStatusTip("Center align text")
        self.align_center_action.triggered.connect(lambda: handlers.set_align_center(self)) # ربط الدالة الجديدة
        alignment_menu.addAction(self.align_center_action)

        self.align_right_action = QAction("Align Right", self)
        self.align_right_action.setShortcut("Ctrl+R")
        self.align_right_action.setStatusTip("Align text to the right")
        self.align_right_action.triggered.connect(lambda: handlers.set_align_right(self)) # ربط الدالة الجديدة
        alignment_menu.addAction(self.align_right_action)

        format_menu.addSeparator()

        self.ltr_action = QAction("Left-to-Right", self)
        self.ltr_action.setShortcut("Ctrl+Shift+L")
        self.ltr_action.setStatusTip("Set text direction to Left-to-Right for current block/selection")
        self.ltr_action.triggered.connect(lambda: handlers.set_block_ltr(self)) # ربط الدالة الجديدة
        format_menu.addAction(self.ltr_action)

        self.rtl_action = QAction("Right-to-Left", self)
        self.rtl_action.setShortcut("Ctrl+Shift+R")
        self.rtl_action.setStatusTip("Set text direction to Right-to-Left for current block/selection")
        self.rtl_action.triggered.connect(lambda: handlers.set_block_rtl(self)) # ربط الدالة الجديدة
        format_menu.addAction(self.rtl_action)

        # --- قائمة Help ---
        help_menu = menu_bar.addMenu("Help")

        self.about_action = QAction("About", self)
        self.about_action.setStatusTip("Show application information")
        self.about_action.triggered.connect(lambda: handlers.show_about_dialog(self)) # ربط الدالة الجديدة
        help_menu.addAction(self.about_action)

    def create_tool_bar(self):
        tool_bar = self.addToolBar("Main Toolbar")
        tool_bar.setIconSize(QSize(24, 24))

        tool_bar.addAction(self.new_action)
        tool_bar.addAction(self.open_action)
        tool_bar.addAction(self.save_action)
        tool_bar.addSeparator()

        tool_bar.addAction(self.undo_action)
        tool_bar.addAction(self.redo_action)
        tool_bar.addSeparator()

        self.font_family_combo = QComboBox(self)
        self.font_family_combo.setToolTip("Font Family")
        self.font_family_combo.addItems(QFontDatabase().families())
        self.font_family_combo.setEditable(True)
        # ربط الدالة من handlers.py
        self.font_family_combo.currentIndexChanged.connect(lambda index: handlers.set_font_family(self, index))
        tool_bar.addWidget(self.font_family_combo)

        self.font_size_combo = QComboBox(self)
        self.font_size_combo.setToolTip("Font Size")
        font_sizes = [str(s) for s in [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]]
        self.font_size_combo.addItems(font_sizes)
        self.font_size_combo.setEditable(True)
        # ربط الدالة من handlers.py
        self.font_size_combo.currentIndexChanged.connect(lambda index: handlers.set_font_size(self, index))
        tool_bar.addWidget(self.font_size_combo)
        tool_bar.addSeparator()

        tool_bar.addAction(self.find_action)
        tool_bar.addAction(self.replace_action)


    def create_status_bar(self):
        self.statusBar = self.statusBar()
        self.status_label = QLabel("Ready")
        self.statusBar.addWidget(self.status_label)

        self.count_label = QLabel("Words: 0 | Chars: 0")
        self.statusBar.addPermanentWidget(self.count_label)

    def update_word_char_count(self):
        text = self.text_editor.toPlainText()
        words = len(text.split())
        chars = len(text)
        self.count_label.setText(f"Words: {words} | Chars: {chars}")

    def update_font_info_combos(self):
        cursor = self.text_editor.textCursor()
        current_char_format = cursor.charFormat()

        if hasattr(self, 'font_size_combo'):
            self.font_size_combo.blockSignals(True)
            current_font_size = int(current_char_format.fontPointSize())
            index = self.font_size_combo.findText(str(current_font_size))
            if index != -1:
                self.font_size_combo.setCurrentIndex(index)
            else:
                # لو الحجم مش موجود في القائمة، بنضيفه عشان يظهر
                self.font_size_combo.setEditText(str(current_font_size))
            self.font_size_combo.blockSignals(False)

        if hasattr(self, 'font_family_combo'):
            self.font_family_combo.blockSignals(True)
            current_font_family = current_char_format.fontFamily()
            index = self.font_family_combo.findText(current_font_family)
            if index != -1:
                self.font_family_combo.setCurrentIndex(index)
            else:
                # لو نوع الخط مش موجود في القائمة، بنضيفه عشان يظهر
                self.font_family_combo.setEditText(current_font_family)
            self.font_family_combo.blockSignals(False)

    # دوال Show Dialogs هتفضل هنا لأنها بتنشئ كائنات Dialog
    # وبتتعامل معاها مباشرة (FindDialog(self))
    def show_find_dialog(self):
        self.find_dialog = FindDialog(self)
        self.find_dialog.show()

    def show_find_replace_dialog(self):
        self.find_replace_dialog = FindReplaceDialog(self)
        self.find_replace_dialog.show()

    # keyPressEvent ممكن يفضل هنا أو يتنقل لوظيفية أعمق حسب التعقيد المستقبلي
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
