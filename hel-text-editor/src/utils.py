import os
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize

# المسار الأساسي للمشروع للوصول إلى الملفات مثل الأيقونات.
# بنفترض هنا إن utils.py موجود في src
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_default_icons():
    """
    بيضمن وجود الأيقونات الافتراضية في مجلد assets/icons.
    بينشئ أيقونات شفافة لو مش موجودة أو حجمها مش مظبوط.
    """
    icons_dir = os.path.join(BASE_DIR, "assets", "icons")
    os.makedirs(icons_dir, exist_ok=True)

    icon_files = {
        "app_icon.png": (1, 1),
        "about_icon.png": (1, 1),
        "font_color.png": (24, 24),
        "highlight_color.png": (24, 24),
        "align_left.png": (24, 24),
        "align_center.png": (24, 24),
        "align_right.png": (24, 24)
    }

    for icon_name, size in icon_files.items():
        icon_path = os.path.join(icons_dir, icon_name)
        # Check if the file exists and is not a valid QPixmap or has the wrong size
        if not os.path.exists(icon_path) or QPixmap(icon_path).isNull() or QPixmap(icon_path).size() != QSize(*size):
            dummy_pixmap = QPixmap(*size)
            dummy_pixmap.fill(Qt.transparent) # Keep it transparent for now
            dummy_pixmap.save(icon_path, "PNG")
            print(f"Default icon created or updated at: {icon_path}")
