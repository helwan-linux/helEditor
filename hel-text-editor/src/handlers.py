import os
import re
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QColorDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDialog
from PyQt5.QtGui import QTextCharFormat, QFont, QColor, QTextCursor, QPixmap, QTextDocument, QTextBlockFormat
from PyQt5.QtCore import Qt

# تحديد المسار الأساسي للمشروع
# ده هيخليه يقدر يوصل لـ assets
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def new_file(editor_instance):
    """
    إنشاء ملف جديد: مسح المحتوى، تصفير اسم الملف الحالي، إعادة تعيين اتجاه النص لليسار،
    وتحديث عداد الكلمات والأحرف.
    """
    editor_instance.text_editor.clear()
    editor_instance.current_file = None
    editor_instance.setWindowTitle("Helwan Text Editor")
    # التأكد من إعادة تعيين الاتجاه الافتراضي لليسار عند إنشاء ملف جديد
    set_block_ltr(editor_instance) # استدعاء مباشر لدالة LTR
    editor_instance.update_word_char_count()
    editor_instance.statusBar.showMessage("New file created.", 2000)
    editor_instance.update_font_info_combos()

def open_file(editor_instance):
    """
    فتح ملف موجود وقراءة محتواه.
    تم التعديل لدعم RTF و Text (عبر HTML لـ RTF).
    """
    file_name, file_filter = QFileDialog.getOpenFileName(
        editor_instance,
        "Open File",
        "",
        # تم تغيير الترتيب لجعل RTF هو الخيار الأول
        "Rich Text Files (*.rtf);;Text Files (*.txt);;All Files (*)"
    )

    if file_name:
        try:
            if file_filter == "Rich Text Files (*.rtf)":
                # الطريقة الأكثر موثوقية لفتح RTF هي قراءته كنص عادي ثم استخدام setHtml
                with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    editor_instance.text_editor.setHtml(content) # يحاول تفسير RTF كـ HTML

            elif file_filter == "Text Files (*.txt)":
                with open(file_name, 'r', encoding='utf-8') as f:
                    text = f.read()
                    editor_instance.text_editor.setPlainText(text)
            else: # All Files or other extensions, try to open as text
                 with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                    editor_instance.text_editor.setPlainText(text)

            editor_instance.current_file = file_name
            editor_instance.setWindowTitle(f"Helwan Text Editor - {os.path.basename(file_name)}")

            # تحديد الاتجاه بعد الفتح
            detect_and_set_direction(editor_instance, editor_instance.text_editor.toPlainText())
            editor_instance.update_word_char_count()
            editor_instance.statusBar.showMessage(f"Opened: {os.path.basename(file_name)}", 2000)
            editor_instance.update_font_info_combos()

        except Exception as e:
            editor_instance.statusBar.showMessage(f"Error opening file: {e}", 3000)
            print(f"Error opening file: {e}")

def save_file(editor_instance):
    """
    حفظ الملف الحالي. لو ملوش اسم، هيفتح نافذة Save As.
    تم التعديل لدعم RTF و Text (عبر HTML لـ RTF).
    """
    if editor_instance.current_file:
        try:
            file_extension = os.path.splitext(editor_instance.current_file)[1].lower()
            if file_extension == ".rtf":
                with open(editor_instance.current_file, 'w', encoding='utf-8') as f:
                    # QTextEdit يحول محتواه إلى RTF تلقائياً عند طلب toHtml() (يتم تفسير HTML كـ RTF)
                    f.write(editor_instance.text_editor.toHtml())

            else: # افتراضياً txt أو أي امتداد تاني
                with open(editor_instance.current_file, 'w', encoding='utf-8') as f:
                    f.write(editor_instance.text_editor.toPlainText())

            editor_instance.statusBar.showMessage(f"File saved: {os.path.basename(editor_instance.current_file)}", 2000)
        except Exception as e:
            editor_instance.statusBar.showMessage(f"Error saving file: {e}", 3000)
            print(f"Error saving file: {e}")
    else:
        save_file_as(editor_instance)

def save_file_as(editor_instance):
    """
    حفظ الملف باسم جديد.
    تم التعديل لدعم RTF و Text (عبر HTML لـ RTF).
    """
    file_name, file_filter = QFileDialog.getSaveFileName(
        editor_instance,
        "Save File As",
        "",
        # تم تغيير الترتيب لجعل RTF هو الخيار الأول
        "Rich Text Files (*.rtf);;Text Files (*.txt);;All Files (*)"
    )

    if file_name:
        try:
            if file_filter == "Rich Text Files (*.rtf)":
                if not file_name.lower().endswith(".rtf"):
                    file_name += ".rtf"
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(editor_instance.text_editor.toHtml())

            elif file_filter == "Text Files (*.txt)":
                if not file_name.lower().endswith(".txt"):
                    file_name += ".txt"
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(editor_instance.text_editor.toPlainText())
            else: # لو المستخدم اختار All Files أو ماحددش امتداد، بنحفظه كـ txt افتراضياً
                if not (file_name.lower().endswith(".txt") or file_name.lower().endswith(".rtf")):
                    file_name += ".txt"
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(editor_instance.text_editor.toPlainText())


            editor_instance.current_file = file_name
            editor_instance.setWindowTitle(f"Helwan Text Editor - {os.path.basename(editor_instance.current_file)}")
            editor_instance.statusBar.showMessage(f"File saved as: {os.path.basename(editor_instance.current_file)}", 2000)
        except Exception as e:
            editor_instance.statusBar.showMessage(f"Error saving file as: {e}", 3000)
            print(f"Error saving file as: {e}")

def detect_and_set_direction(editor_instance, text):
    """
    يكشف اتجاه النص (عربي أم إنجليزي) ويضبط اتجاه المحرر تلقائيًا.
    """
    arabic_characters_pattern = re.compile(r'[\u0600-\u06FF]')

    arabic_char_count = len(arabic_characters_pattern.findall(text))
    total_chars = len(text)

    if total_chars > 0 and (arabic_char_count / total_chars) > 0.25:
        set_block_rtl(editor_instance)
        editor_instance.statusBar.showMessage("Detected RTL text. Direction set to Right-to-Left.", 2000)
    else:
        set_block_ltr(editor_instance)
        editor_instance.statusBar.showMessage("Detected LTR text. Direction set to Left-to-Right.", 2000)

def set_block_ltr(editor_instance):
    """
    يضبط اتجاه النص للكتلة الحالية من اليسار لليمين.
    """
    cursor = editor_instance.text_editor.textCursor()
    current_position = cursor.position()
    
    cursor.beginEditBlock()
    
    new_block_format = QTextBlockFormat()
    new_block_format.setLayoutDirection(Qt.LeftToRight)
    new_block_format.setAlignment(Qt.AlignLeft)

    if cursor.hasSelection():
        # لتطبيق التنسيق على كل الفقرات المحددة
        start_cursor = editor_instance.text_editor.textCursor()
        start_cursor.setPosition(cursor.selectionStart())
        start_block = start_cursor.blockNumber()
        
        end_cursor = editor_instance.text_editor.textCursor()
        end_cursor.setPosition(cursor.selectionEnd())
        end_block = end_cursor.blockNumber()

        temp_cursor = editor_instance.text_editor.textCursor()
        temp_cursor.setPosition(cursor.selectionStart()) # ابدأ من بداية التحديد
        
        while True:
            temp_cursor.mergeBlockFormat(new_block_format)
            if temp_cursor.blockNumber() >= end_block:
                break
            temp_cursor.movePosition(QTextCursor.NextBlock)
    else:
        # لو مفيش تحديد، بنطبق على الفقرة اللي فيها المؤشر
        cursor.mergeBlockFormat(new_block_format)
    
    cursor.endEditBlock()
    
    # إعادة المؤشر إلى مكانه الأصلي
    cursor.setPosition(current_position)
    editor_instance.text_editor.setTextCursor(cursor)
    
    editor_instance.statusBar.showMessage("Text direction set to Left-to-Right.", 2000)


def set_block_rtl(editor_instance):
    """
    يضبط اتجاه النص للكتلة الحالية من اليمين لليسار.
    """
    cursor = editor_instance.text_editor.textCursor()
    current_position = cursor.position()

    cursor.beginEditBlock()

    new_block_format = QTextBlockFormat()
    new_block_format.setLayoutDirection(Qt.RightToLeft)
    new_block_format.setAlignment(Qt.AlignRight)

    if cursor.hasSelection():
        # لتطبيق التنسيق على كل الفقرات المحددة
        start_cursor = editor_instance.text_editor.textCursor()
        start_cursor.setPosition(cursor.selectionStart())
        start_block = start_cursor.blockNumber()
        
        end_cursor = editor_instance.text_editor.textCursor()
        end_cursor.setPosition(cursor.selectionEnd())
        end_block = end_cursor.blockNumber()

        temp_cursor = editor_instance.text_editor.textCursor()
        temp_cursor.setPosition(cursor.selectionStart()) # ابدأ من بداية التحديد
        
        while True:
            temp_cursor.mergeBlockFormat(new_block_format)
            if temp_cursor.blockNumber() >= end_block:
                break
            temp_cursor.movePosition(QTextCursor.NextBlock)
    else:
        # لو مفيش تحديد، بنطبق على الفقرة اللي فيها المؤشر
        cursor.mergeBlockFormat(new_block_format)

    cursor.endEditBlock()

    # إعادة المؤشر إلى مكانه الأصلي
    cursor.setPosition(current_position)
    editor_instance.text_editor.setTextCursor(cursor)

    editor_instance.statusBar.showMessage("Text direction set to Right-to-Left.", 2000)

def set_bold(editor_instance):
    """
    يجعل النص المحدد (أو النص الجديد) غامقًا أو عاديًا.
    """
    cursor = editor_instance.text_editor.textCursor()
    current_format = cursor.charFormat()
    new_format = QTextCharFormat(current_format)

    new_format.setFontWeight(QFont.Normal if current_format.fontWeight() == QFont.Bold else QFont.Bold)

    if cursor.hasSelection():
        cursor.mergeCharFormat(new_format)
        editor_instance.statusBar.showMessage("Selected text bold/normal.", 2000)
    else:
        editor_instance.text_editor.setCurrentCharFormat(new_format)
        editor_instance.statusBar.showMessage("Toggled bold for new text.", 2000)


def set_italic(editor_instance):
    """
    يجعل النص المحدد (أو النص الجديد) مائلاً أو عاديًا.
    """
    cursor = editor_instance.text_editor.textCursor()
    current_format = cursor.charFormat()
    new_format = QTextCharFormat(current_format)

    new_format.setFontItalic(not current_format.fontItalic())

    if cursor.hasSelection():
        cursor.mergeCharFormat(new_format)
        editor_instance.statusBar.showMessage("Selected text italic/normal.", 2000)
    else:
        editor_instance.text_editor.setCurrentCharFormat(new_format)
        editor_instance.statusBar.showMessage("Toggled italic for new text.", 2000)

def set_underline(editor_instance):
    """
    يجعل النص المحدد (أو النص الجديد) تحته خط أو عاديًا.
    """
    cursor = editor_instance.text_editor.textCursor()
    current_format = cursor.charFormat()
    new_format = QTextCharFormat(current_format)

    new_format.setFontUnderline(not current_format.fontUnderline())

    if cursor.hasSelection():
        cursor.mergeCharFormat(new_format)
        editor_instance.statusBar.showMessage("Selected text underlined/normal.", 2000)
    else:
        editor_instance.text_editor.setCurrentCharFormat(new_format)
        editor_instance.statusBar.showMessage("Toggled underline for new text.", 2000)

def set_font_size(editor_instance, index=None):
    """
    يضبط حجم الخط للنص المحدد (أو النص الجديد).
    """
    try:
        font_size_str = editor_instance.font_size_combo.currentText()
        font_size = float(font_size_str)

        cursor = editor_instance.text_editor.textCursor()
        char_format = QTextCharFormat(cursor.charFormat())
        char_format.setFontPointSize(font_size)

        if cursor.hasSelection():
            cursor.mergeCharFormat(char_format)
            editor_instance.statusBar.showMessage(f"Font size set to {font_size} for selected text.", 2000)
        else:
            editor_instance.text_editor.setCurrentCharFormat(char_format)
            editor_instance.statusBar.showMessage(f"Default font size set to {font_size}.", 2000)

    except ValueError:
        editor_instance.statusBar.showMessage("Invalid font size. Please enter a number.", 2000)
    except Exception as e:
        editor_instance.statusBar.showMessage(f"Error setting font size: {e}", 3000)
        print(f"Error setting font size: {e}")

def set_font_color(editor_instance):
    """
    يغير لون الخط للنص المحدد (أو النص الجديد).
    """
    current_color = editor_instance.text_editor.textCursor().charFormat().foreground().color()
    color = QColorDialog.getColor(current_color, editor_instance, "Select Font Color")
    if color.isValid():
        cursor = editor_instance.text_editor.textCursor()
        char_format = QTextCharFormat(cursor.charFormat())
        char_format.setForeground(QColor(color))

        if cursor.hasSelection():
            cursor.mergeCharFormat(char_format)
            editor_instance.statusBar.showMessage(f"Font color changed to {color.name()} for selected text.", 2000)
        else:
            editor_instance.text_editor.setCurrentCharFormat(char_format) # تم تصحيح هذا السطر
            editor_instance.statusBar.showMessage(f"Default font color set to {color.name()}.", 2000)

def set_text_background_color(editor_instance):
    """
    يغير لون خلفية النص (التظليل) للنص المحدد (أو النص الجديد).
    """
    current_color = editor_instance.text_editor.textCursor().charFormat().background().color()
    color = QColorDialog.getColor(current_color, editor_instance, "Select Highlight Color")
    if color.isValid():
        cursor = editor_instance.text_editor.textCursor()
        char_format = QTextCharFormat(cursor.charFormat())
        char_format.setBackground(QColor(color))

        if cursor.hasSelection():
            cursor.mergeCharFormat(char_format)
            editor_instance.statusBar.showMessage(f"Highlight color changed to {color.name()} for selected text.", 2000)
        else:
            editor_instance.text_editor.setCurrentCharFormat(char_format) # تم تصحيح هذا السطر
            editor_instance.statusBar.showMessage(f"Default highlight color set to {color.name()}.", 2000)

def set_font_family(editor_instance, index):
    """
    يضبط نوع الخط للنص المحدد (أو النص الجديد).
    """
    font_family = editor_instance.font_family_combo.currentText()
    cursor = editor_instance.text_editor.textCursor()
    char_format = QTextCharFormat(cursor.charFormat())
    char_format.setFontFamily(font_family)

    if cursor.hasSelection():
        cursor.mergeCharFormat(char_format)
        editor_instance.statusBar.showMessage(f"Font family set to '{font_family}' for selected text.", 2000)
    else:
        editor_instance.text_editor.setCurrentCharFormat(char_format) # تم تصحيح هذا السطر
        editor_instance.statusBar.showMessage(f"Default font family set to '{font_family}'.", 2000)

def set_align_left(editor_instance):
    """
    يضبط محاذاة الفقرة الحالية إلى اليسار.
    """
    cursor = editor_instance.text_editor.textCursor()
    block_format = cursor.blockFormat()
    block_format.setAlignment(Qt.AlignLeft)
    cursor.setBlockFormat(block_format)
    editor_instance.text_editor.setTextCursor(cursor)
    editor_instance.statusBar.showMessage("Text aligned left.", 2000)

def set_align_center(editor_instance):
    """
    يضبط محاذاة الفقرة الحالية إلى الوسط.
    """
    cursor = editor_instance.text_editor.textCursor()
    block_format = cursor.blockFormat()
    block_format.setAlignment(Qt.AlignCenter)
    cursor.setBlockFormat(block_format)
    editor_instance.text_editor.setTextCursor(cursor)
    editor_instance.statusBar.showMessage("Text aligned center.", 2000)

def set_align_right(editor_instance):
    """
    يضبط محاذاة الفقرة الحالية إلى اليمين.
    """
    cursor = editor_instance.text_editor.textCursor()
    block_format = cursor.blockFormat()
    block_format.setAlignment(Qt.AlignRight)
    cursor.setBlockFormat(block_format)
    editor_instance.text_editor.setTextCursor(cursor)
    editor_instance.statusBar.showMessage("Text aligned right.", 2000)

def show_about_dialog(editor_instance):
    """
    يظهر نافذة "حول" التطبيق.
    """
    about_dialog = QDialog(editor_instance)
    about_dialog.setWindowTitle("About")
    about_dialog.setFixedSize(300, 250)

    about_layout = QVBoxLayout()

    about_icon_path = os.path.join(BASE_DIR, "assets", "icons", "about_icon.png")
    temp_pixmap = QPixmap()
    if os.path.exists(about_icon_path):
        temp_pixmap.load(about_icon_path)

    if not temp_pixmap.isNull():
        about_icon_pixmap = temp_pixmap.scaledToWidth(64, Qt.SmoothTransformation)
    else:
        print(f"Warning: About icon not found or invalid at: {about_icon_path}. Using default transparent icon.")
        about_icon_pixmap = QPixmap(1, 1)
        about_icon_pixmap.fill(Qt.transparent)

    icon_label = QLabel()
    icon_label.setPixmap(about_icon_pixmap)
    icon_label.setAlignment(Qt.AlignCenter)
    about_layout.addWidget(icon_label)

    about_layout.addWidget(QLabel("<h1>Helwan Text Editor</h1>", alignment=Qt.AlignCenter))
    about_layout.addWidget(QLabel("<b>Version:</b> 0.1 Beta", alignment=Qt.AlignCenter))
    about_layout.addWidget(QLabel("Developed by Helwan Linux Team", alignment=Qt.AlignCenter))
    about_layout.addWidget(QLabel("Providing a unique Arabic text editing experience.", alignment=Qt.AlignCenter))

    close_button = QPushButton("Close")
    close_button.clicked.connect(about_dialog.accept)
    about_layout.addWidget(close_button, alignment=Qt.AlignCenter)

    about_dialog.setLayout(about_layout)
    about_dialog.exec_()
