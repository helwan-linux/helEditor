# Maintainer: Saeed Badrelden <you@example.com>
pkgname=hel-text-editor
pkgver=1.0.0
pkgrel=1
pkgdesc="A lightweight Python-based text editor for Helwan Linux."
arch=('any')
url="https://github.com/helwan-linux/helEditor"
license=('GPL3')
depends=('python' 'python-pyqt5')
source=("https://github.com/helwan-linux/helEditor/archive/refs/heads/main.zip")
md5sums=('SKIP')

build() {
  echo "No build step required."
}

package() {
  cd "$srcdir/helEditor-main/hel-text-editor"

  # نسخ ملفات البرنامج إلى /opt
  install -d "$pkgdir/opt/$pkgname"
  cp -r src "$pkgdir/opt/$pkgname/"
  cp -r assets "$pkgdir/opt/$pkgname/"

  # إنشاء ملف desktop
  install -Dm644 /dev/stdin "$pkgdir/usr/share/applications/hel-text-editor.desktop" <<EOF
[Desktop Entry]
Name=Hel Text Editor
Comment=Simple and fast text editor written in Python
Exec=python3 /opt/$pkgname/src/main.py
Icon=/opt/$pkgname/assets/images/splash_screen.png
Terminal=false
Type=Application
Categories=Utility;TextEditor;
EOF
}

