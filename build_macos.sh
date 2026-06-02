#!/bin/bash
set -e

echo "========================================="
echo "   Building Avelyn macOS .app Bundle     "
echo "========================================="

# 1. Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist
rm -rf assets/icon.icns assets/icon.iconset

# 2. Generate .icns file if public/logo.png exists
if [ -f "public/logo.png" ]; then
    echo "🎨 Copying master public/logo.png to assets/icon.png..."
    mkdir -p assets
    cp public/logo.png assets/icon.png

    echo "🎨 Generating high-res macOS icon (.icns) from public/logo.png..."
    mkdir -p assets/icon.iconset
    sips -s format png -z 16 16     public/logo.png --out assets/icon.iconset/icon_16x16.png
    sips -s format png -z 32 32     public/logo.png --out assets/icon.iconset/icon_16x16@2x.png
    sips -s format png -z 32 32     public/logo.png --out assets/icon.iconset/icon_32x32.png
    sips -s format png -z 64 64     public/logo.png --out assets/icon.iconset/icon_32x32@2x.png
    sips -s format png -z 128 128   public/logo.png --out assets/icon.iconset/icon_128x128.png
    sips -s format png -z 256 256   public/logo.png --out assets/icon.iconset/icon_128x128@2x.png
    sips -s format png -z 256 256   public/logo.png --out assets/icon.iconset/icon_256x256.png
    sips -s format png -z 512 512   public/logo.png --out assets/icon.iconset/icon_256x256@2x.png
    sips -s format png -z 512 512   public/logo.png --out assets/icon.iconset/icon_512x512.png
    sips -s format png -z 1024 1024 public/logo.png --out assets/icon.iconset/icon_512x512@2x.png
    iconutil -c icns assets/icon.iconset
    rm -rf assets/icon.iconset
else
    echo "⚠️  public/logo.png not found. App will use default icon."
fi

# 3. Run PyInstaller
echo "📦 Packaging with PyInstaller..."
.venv/bin/python -m PyInstaller --clean Avelyn.spec

echo "========================================="
echo "✅ Build Complete!"
echo "You can find your standalone app at: dist/Avelyn.app"
echo "To test it, simply double-click it in Finder."
echo "========================================="
