from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QTextCursor

# -------------------------------------------------------------
# كلاس لنافذة البحث (Find Dialog)
class FindDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find")
        self.setGeometry(100, 100, 300, 100)
        self.parent_editor = parent # ده هيكون مرجع للـ QTextEdit في الـ MainWindow
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        form_layout = QHBoxLayout()
        self.find_label = QLabel("Find:")
        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("Enter text to find...")
        form_layout.addWidget(self.find_label)
        form_layout.addWidget(self.find_input)
        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.find_button = QPushButton("Find Next")
        self.find_button.clicked.connect(self.find_next)
        button_layout.addStretch(1)
        button_layout.addWidget(self.find_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def find_next(self):
        text_to_find = self.find_input.text()
        if not text_to_find:
            return

        editor = self.parent_editor.text_editor
        cursor = editor.textCursor()

        start_position = cursor.selectionEnd() if cursor.hasSelection() else cursor.position()
        editor.setTextCursor(cursor)

        found = editor.find(text_to_find)

        if not found:
            cursor.setPosition(0)
            editor.setTextCursor(cursor)
            found = editor.find(text_to_find)

            if not found:
                QMessageBox.information(self, "Find", f"'{text_to_find}' not found from beginning.")
            else:
                QMessageBox.information(self, "Find", f"Reached end of document. Continuing search from beginning. Found '{text_to_find}'.")

# -------------------------------------------------------------
# كلاس لنافذة البحث والاستبدال (Find/Replace Dialog)
class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find and Replace")
        self.setGeometry(100, 100, 350, 150)
        self.parent_editor = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        find_layout = QHBoxLayout()
        self.find_label = QLabel("Find:")
        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("Enter text to find...")
        find_layout.addWidget(self.find_label)
        find_layout.addWidget(self.find_input)
        layout.addLayout(find_layout)

        replace_layout = QHBoxLayout()
        self.replace_label = QLabel("Replace with:")
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Enter replacement text...")
        replace_layout.addWidget(self.replace_label)
        replace_layout.addWidget(self.replace_input)
        layout.addLayout(replace_layout)

        button_layout = QHBoxLayout()
        self.find_next_button = QPushButton("Find Next")
        self.find_next_button.clicked.connect(self.find_next)

        self.replace_button = QPushButton("Replace")
        self.replace_button.clicked.connect(self.replace_one)

        self.replace_all_button = QPushButton("Replace All")
        self.replace_all_button.clicked.connect(self.replace_all)

        button_layout.addStretch(1)
        button_layout.addWidget(self.find_next_button)
        button_layout.addWidget(self.replace_button)
        button_layout.addWidget(self.replace_all_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def find_next(self):
        text_to_find = self.find_input.text()
        if not text_to_find:
            return

        editor = self.parent_editor.text_editor
        cursor = editor.textCursor()

        start_position = cursor.selectionEnd() if cursor.hasSelection() else cursor.position()
        editor.setTextCursor(cursor)

        found = editor.find(text_to_find)

        if not found:
            cursor.setPosition(0)
            editor.setTextCursor(cursor)
            found = editor.find(text_to_find)

            if not found:
                QMessageBox.information(self, "Find", f"'{text_to_find}' not found from beginning.")
            else:
                QMessageBox.information(self, "Find", f"Reached end of document. Continuing search from beginning. Found '{text_to_find}'.")

    def replace_one(self):
        text_to_find = self.find_input.text()
        replace_with = self.replace_input.text()
        if not text_to_find:
            return

        editor = self.parent_editor.text_editor
        cursor = editor.textCursor()

        if cursor.hasSelection() and cursor.selectedText() == text_to_find:
            cursor.removeSelectedText()
            cursor.insertText(replace_with)
            editor.setTextCursor(cursor)
            self.find_next()
        else:
            self.find_next()
            cursor = editor.textCursor()
            if cursor.hasSelection() and cursor.selectedText() == text_to_find:
                cursor.removeSelectedText()
                cursor.insertText(replace_with)
                editor.setTextCursor(cursor)


    def replace_all(self):
        text_to_find = self.find_input.text()
        replace_with = self.replace_input.text()
        if not text_to_find:
            return

        editor = self.parent_editor.text_editor
        document = editor.document()
        cursor = QTextCursor(document)
        editor.setTextCursor(cursor)

        count = 0

        while True:
            found = editor.find(text_to_find)
            if found:
                current_cursor = editor.textCursor()
                current_cursor.removeSelectedText()
                current_cursor.insertText(replace_with)
                editor.setTextCursor(current_cursor)
                count += 1
            else:
                break

        QMessageBox.information(self, "Replace All", f"Replaced {count} occurrences of '{text_to_find}'.")
