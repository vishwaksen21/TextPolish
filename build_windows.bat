@echo off
echo =========================================
echo  Building TextPolish Windows .exe
echo =========================================

echo 🧹 Cleaning previous builds...
rmdir /S /Q build
rmdir /S /Q dist

echo 🎨 Generating Windows icon (.ico)...
python -c "from PIL import Image; import os; img = Image.open('assets/icon.png') if os.path.exists('assets/icon.png') else None; img.save('assets/icon.ico', format='ICO', sizes=[(256,256)]) if img else print('No icon.png found')"

echo 📦 Packaging with PyInstaller...
pyinstaller --clean TextPolish.spec

echo =========================================
echo ✅ Build Complete!
echo You can find your standalone executable at: dist\TextPolish\TextPolish.exe
echo =========================================
pause
