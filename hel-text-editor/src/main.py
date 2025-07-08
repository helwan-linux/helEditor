import sys
import os
from PyQt5.QtWidgets import QApplication

# تحديد المسار الأساسي للمشروع
# ده هيخلي بايثون تعرف تدور على الملفات في مجلد src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# استيراد الوظائف من الملفات الجديدة باستخدام المسار المطلق
from src.main_window import MainWindow
from src.utils import create_default_icons


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # أولًا: التأكد من وجود الأيقونات الافتراضية
    create_default_icons()

    # ثانيًا: إنشاء نافذة التطبيق الرئيسية وتشغيلها
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
