@echo off
echo =========================================
echo  Building Avelyn Windows .exe
echo =========================================

echo 🧹 Cleaning previous builds...
rmdir /S /Q build
rmdir /S /Q dist

echo 🎨 Generating Windows icon (.ico) from public/logo.png...
if not exist assets mkdir assets
copy public\logo.png assets\icon.png /Y
python -c "from PIL import Image; import os; img = Image.open('public/logo.png') if os.path.exists('public/logo.png') else None; img.save('assets/icon.ico', format='ICO', sizes=[(256,256)]) if img else print('No logo.png found')"

echo 📦 Packaging with PyInstaller...
pyinstaller --clean Avelyn.spec

echo =========================================
echo ✅ Build Complete!
echo You can find your standalone executable at: dist\Avelyn\Avelyn.exe
echo =========================================
if not "%GITHUB_ACTIONS%"=="true" pause
