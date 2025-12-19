# 🔧 Troubleshooting - Errores de Compilación

## Errores Comunes y Soluciones

### ❌ Error 1: "ModuleNotFoundError: No module named 'XXX'"

**Causa**: Falta una dependencia en el sistema

**Solución**:
```bash
# Instalar todas las dependencias
pip install -r /app/backend/requirements.txt
pip install pillow pynput pyinstaller

# O instalar la específica que falta
pip install <nombre_modulo>
```

---

### ❌ Error 2: "WARNING: Failed to collect submodules for 'pynput'"

**Causa**: pynput requiere X11 en Linux, pero estamos en un servidor headless

**Solución**: Este es solo un WARNING, no detiene la compilación. El ejecutable funcionará correctamente en sistemas con interfaz gráfica (Windows/Linux Desktop).

**¿Qué significa?**
- El keylogger NO funcionará en el servidor de compilación
- PERO SÍ funcionará en el target Windows/Linux Desktop
- Es normal y esperado

---

### ❌ Error 3: "Permission denied" al escribir en /app/payloads

**Solución**:
```bash
# Crear directorio con permisos
sudo mkdir -p /app/payloads
sudo chmod 777 /app/payloads

# O cambiar owner
sudo chown -R $(whoami):$(whoami) /app/payloads
```

---

### ❌ Error 4: PyInstaller no encontrado

**Solución**:
```bash
# Instalar PyInstaller
pip install pyinstaller

# Verificar instalación
pyinstaller --version

# Si sigue fallando, usar path completo
python3 -m PyInstaller --version
```

---

### ❌ Error 5: "ImportError: this platform is not supported"

**Causa**: Compilando para plataforma incorrecta

**Solución**:
- Si compilas en Linux, el .exe NO funcionará
- Necesitas compilar en Windows para generar .exe

**Opciones**:
1. **Compilar en Windows** (recomendado para .exe)
2. **Cross-compile** (complejo, no recomendado)
3. **Usar Wine** (puede funcionar)

---

### ❌ Error 6: Payload muy grande (>50MB)

**Causa**: PyInstaller incluye muchas librerías

**Solución**:
```bash
# Compilar con UPX compression
pyinstaller --onefile --noconsole --upx-dir=/usr/bin agent_advanced.py

# O excluir módulos no necesarios
pyinstaller --onefile --noconsole \
  --exclude-module matplotlib \
  --exclude-module pandas \
  agent_advanced.py
```

---

### ❌ Error 7: "Failed to execute script" al correr el .exe

**Causa**: Falta una DLL o el antivirus lo bloqueó

**Solución**:
```bash
# Compilar en modo console para ver errores
pyinstaller --onefile agent_advanced.py
# (sin --noconsole)

# Luego ejecutar y ver el error específico
```

---

### ❌ Error 8: Builder desde Dashboard no funciona

**Causa**: Problema con rutas o permisos

**Solución Manual**:
```bash
# Usar script manual en su lugar
bash /app/build_payload_manual.sh

# O compilar directamente
cd /app
pyinstaller --onefile --noconsole agent_advanced.py
```

**Verificar backend logs**:
```bash
tail -f /var/log/supervisor/backend.err.log
```

---

## 🔍 Diagnóstico Paso a Paso

### Paso 1: Verificar Dependencias

```bash
python3 << 'EOF'
import sys
modules = [
    'websockets',
    'Crypto',
    'psutil', 
    'requests',
    'PIL',
    'pynput',
    'PyInstaller'
]

missing = []
for mod in modules:
    try:
        __import__(mod)
        print(f"✓ {mod}")
    except ImportError:
        print(f"✗ {mod} - MISSING")
        missing.append(mod)

if missing:
    print(f"\nInstall missing: pip install {' '.join(missing)}")
    sys.exit(1)
else:
    print("\n✓ All dependencies installed")
EOF
```

### Paso 2: Compilación de Prueba

```bash
# Crear script de prueba simple
cat > /tmp/test_agent.py << 'EOF'
import websockets
print("Test successful")
EOF

# Compilar
pyinstaller --onefile /tmp/test_agent.py

# Si funciona, el problema está en el código
# Si falla, el problema es PyInstaller/sistema
```

### Paso 3: Verificar PyInstaller

```bash
# Version
pyinstaller --version

# Help
pyinstaller --help

# Test básico
echo "print('hello')" > /tmp/test.py
pyinstaller --onefile /tmp/test.py
```

---

## 🛠️ Métodos de Compilación

### Método 1: Script Manual (Recomendado)

```bash
bash /app/build_payload_manual.sh
```

**Ventajas:**
- Mejor manejo de errores
- Logs detallados
- Limpieza automática

### Método 2: Dashboard Builder

```bash
# Desde el navegador
Dashboard > Builder tab > Generate Payload
```

**Ventajas:**
- Interfaz gráfica
- Configuración fácil
- Integrado en workflow

### Método 3: PyInstaller Directo

```bash
cd /app

pyinstaller \
  --onefile \
  --noconsole \
  --name "my_payload" \
  --distpath /app/payloads \
  agent_advanced.py
```

**Ventajas:**
- Control total
- Opciones avanzadas
- Debugging más fácil

---

## 🎯 Opciones Avanzadas de PyInstaller

### Reducir Tamaño del Ejecutable

```bash
# Básico
pyinstaller --onefile agent_advanced.py

# Con UPX compression
pyinstaller --onefile --upx-dir=/usr/bin agent_advanced.py

# Excluir módulos innecesarios
pyinstaller --onefile \
  --exclude-module matplotlib \
  --exclude-module pandas \
  --exclude-module numpy \
  agent_advanced.py
```

### Ocultar Consola (Stealth)

```bash
# Windows - sin ventana de consola
pyinstaller --onefile --noconsole agent_advanced.py

# Añadir icono personalizado
pyinstaller --onefile --noconsole --icon=icon.ico agent_advanced.py
```

### Debug Mode

```bash
# Modo console para ver errores
pyinstaller --onefile agent_advanced.py

# Con logs detallados
pyinstaller --onefile --log-level DEBUG agent_advanced.py

# Mantener archivos temporales
pyinstaller --onefile --clean agent_advanced.py
```

---

## 📊 Verificar Payload Generado

### Check 1: Archivo Existe

```bash
ls -lh /app/payloads/

# Debe mostrar el .exe con tamaño razonable (15-40 MB)
```

### Check 2: Es Ejecutable

```bash
file /app/payloads/payload_*.exe

# Debe decir: "executable" o similar
```

### Check 3: Dependencias Incluidas

```bash
# En Windows, verificar con Dependency Walker
# En Linux, usar:
ldd /app/payloads/payload_* 2>/dev/null || echo "Es un .exe de Windows"
```

---

## 🐞 Debug del Payload

### Ejecutar con Logs

```bash
# En target, ejecutar desde terminal
./payload_xxx.exe

# Debería mostrar:
# "C2 Framework Advanced Agent - Starting..."
# Si no aparece nada, hay un error
```

### Verificar Conexión

```bash
# En servidor C2, ver logs
tail -f /var/log/supervisor/backend.out.log

# Debe aparecer:
# "Node [ID] connected"
```

### Test de Funcionalidades

```python
# Probar módulos individualmente
python3 << 'EOF'
from PIL import ImageGrab
print("PIL works")

from pynput import keyboard  
print("pynput works")
EOF
```

---

## 🔧 Soluciones Específicas por Plataforma

### Windows Target

**Compilar en Windows:**
```cmd
pip install pyinstaller
pyinstaller --onefile --noconsole agent_advanced.py
```

**Cross-compile desde Linux (experimental):**
```bash
# Instalar wine
apt-get install wine wine64

# Instalar Python en wine
wine python-3.11-installer.exe

# Compilar
wine python -m PyInstaller --onefile agent_advanced.py
```

### Linux Target

```bash
# Compilar en Linux
pyinstaller --onefile agent_advanced.py

# El binario funcionará en Linux similar
```

### Mac Target

```bash
# Compilar en Mac
pyinstaller --onefile agent_advanced.py

# Para crear .app bundle
pyinstaller --onefile --windowed agent_advanced.py
```

---

## 📝 Checklist de Compilación

Antes de compilar, verificar:

- [ ] Python 3.8+ instalado
- [ ] PyInstaller instalado (`pip install pyinstaller`)
- [ ] Todas las dependencias instaladas
- [ ] Permisos de escritura en `/app/payloads`
- [ ] Espacio suficiente en disco (>100MB libre)
- [ ] AES_KEY configurada en `agent_advanced.py`
- [ ] C2_SERVER URL correcta

Durante compilación:

- [ ] No hay errores (solo warnings está OK)
- [ ] Proceso completa sin interrupciones
- [ ] Archivo .exe generado en `/app/payloads`
- [ ] Tamaño razonable (15-50 MB)

Después de compilar:

- [ ] Archivo es ejecutable
- [ ] Transferir a target
- [ ] Probar ejecución
- [ ] Verificar aparece en dashboard
- [ ] Probar funcionalidades básicas

---

## 🚨 Si Nada Funciona

### Opción 1: Usar Agente Python Directo

```bash
# En lugar de .exe, usar Python directamente
python3 /app/agent_advanced.py
```

**Ventajas:**
- No necesita compilación
- Más fácil de debuggear
- Funciona en cualquier OS con Python

**Desventajas:**
- Requiere Python instalado en target
- Más fácil de detectar
- Dependencias visibles

### Opción 2: Usar Docker para Compilar

```dockerfile
# Dockerfile para compilación
FROM python:3.11
RUN pip install pyinstaller websockets pycryptodome psutil requests pillow pynput
COPY agent_advanced.py /app/
WORKDIR /app
RUN pyinstaller --onefile agent_advanced.py
```

### Opción 3: Compilación en Nube

Usar servicios como:
- GitHub Actions
- GitLab CI
- CircleCI

Con Windows runners para generar .exe

---

## 📞 Obtener Ayuda

Si sigues teniendo problemas:

1. **Revisar logs completos**:
   ```bash
   cat /tmp/build_log_*.txt
   ```

2. **Buscar error específico**: 
   Google: "PyInstaller [tu error específico]"

3. **Verificar versión PyInstaller**:
   ```bash
   pip install --upgrade pyinstaller
   ```

4. **Probar en sistema limpio**:
   - VM nueva
   - Instalar solo lo necesario
   - Compilar de nuevo

---

## ✅ Verificación Final

Si la compilación fue exitosa:

```bash
# Debe existir
ls /app/payloads/payload_*.exe

# Debe tener tamaño
du -h /app/payloads/payload_*.exe

# Debe ser ejecutable (en Windows)
file /app/payloads/payload_*.exe
```

**Output esperado:**
```
/app/payloads/payload_20251218_195357.exe: PE32 executable
Size: 37M
```

---

🛡️ **Recuerda: Estos payloads son para uso autorizado únicamente**
