#!/bin/bash
set -e

echo "========================================="
echo " Building TextPolish macOS .app Bundle "
echo "========================================="

# 1. Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist
rm -rf assets/icon.icns assets/icon.iconset

# 2. Generate .icns file if icon.png exists
if [ -f "assets/icon.png" ]; then
    echo "🎨 Generating high-res macOS icon (.icns)..."
    mkdir assets/icon.iconset
    sips -s format png -z 16 16     assets/icon.png --out assets/icon.iconset/icon_16x16.png
    sips -s format png -z 32 32     assets/icon.png --out assets/icon.iconset/icon_16x16@2x.png
    sips -s format png -z 32 32     assets/icon.png --out assets/icon.iconset/icon_32x32.png
    sips -s format png -z 64 64     assets/icon.png --out assets/icon.iconset/icon_32x32@2x.png
    sips -s format png -z 128 128   assets/icon.png --out assets/icon.iconset/icon_128x128.png
    sips -s format png -z 256 256   assets/icon.png --out assets/icon.iconset/icon_128x128@2x.png
    sips -s format png -z 256 256   assets/icon.png --out assets/icon.iconset/icon_256x256.png
    sips -s format png -z 512 512   assets/icon.png --out assets/icon.iconset/icon_256x256@2x.png
    sips -s format png -z 512 512   assets/icon.png --out assets/icon.iconset/icon_512x512.png
    sips -s format png -z 1024 1024 assets/icon.png --out assets/icon.iconset/icon_512x512@2x.png
    iconutil -c icns assets/icon.iconset
    rm -rf assets/icon.iconset
else
    echo "⚠️  assets/icon.png not found. App will use default icon."
fi

# 3. Run PyInstaller
echo "📦 Packaging with PyInstaller..."
source .venv/bin/activate
pyinstaller --clean TextPolish.spec

echo "========================================="
echo "✅ Build Complete!"
echo "You can find your standalone app at: dist/TextPolish.app"
echo "To test it, simply double-click it in Finder."
echo "========================================="
