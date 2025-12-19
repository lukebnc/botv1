#!/bin/bash

# Script para compilar el agente a ejecutable
# Requiere PyInstaller

echo "========================================="
echo "   C2 Agent Builder"
echo "========================================="
echo ""

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "[INSTALL] PyInstaller no encontrado. Instalando..."
    pip install pyinstaller
fi

# Create build directory
mkdir -p /app/build

echo "[BUILD] Compilando agente a ejecutable..."

# Build for current platform
pyinstaller --onefile \
    --name c2_agent \
    --clean \
    --distpath /app/build \
    --workpath /tmp/build \
    --specpath /tmp \
    /app/agent.py

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "   ✓ Build Exitoso!"
    echo "========================================="
    echo ""
    echo "Ejecutable generado en: /app/build/c2_agent"
    echo ""
    echo "Uso:"
    echo "  ./build/c2_agent"
    echo ""
    echo "Notas:"
    echo "  - El ejecutable incluye todas las dependencias"
    echo "  - Tamaño aproximado: 15-20 MB"
    echo "  - Compatible con la plataforma actual"
    echo ""
    echo "Para Windows (desde Linux):"
    echo "  pyinstaller --onefile --target-architecture=win_amd64 agent.py"
    echo ""
else
    echo ""
    echo "[ERROR] Build falló. Revisa los errores arriba."
fi
