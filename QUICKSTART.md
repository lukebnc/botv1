# ⚡ Quick Start Guide - C2 Framework

## 🚦 Paso a Paso en 5 Minutos

### ✅ Paso 1: Verificar Servicios (30 segundos)

```bash
sudo supervisorctl status
```

**Resultado esperado:**
```
backend      RUNNING
frontend     RUNNING
mongodb      RUNNING
```

Si algo no está corriendo:
```bash
sudo supervisorctl restart all
```

---

### ✅ Paso 2: Probar el Sistema (30 segundos)

```bash
bash /app/test_c2.sh
```

Todos los tests deben mostrar ✓ (verde).

---

### ✅ Paso 3: Acceder al Dashboard (1 minuto)

1. **Abrir navegador**: http://localhost:3000
2. **Login**:
   - Usuario: `admin`
   - Contraseña: `c2admin123`
3. **Ver Dashboard**: Deberías ver estadísticas en 0

---

### ✅ Paso 4: Ejecutar el Agente (1 minuto)

**Terminal Nueva:**
```bash
python3 /app/agent.py
```

**Verás algo como:**
```
============================================================
C2 Framework Agent - Starting...
============================================================
[SUCCESS] Registered with C2 - Node ID: abc123...
[CONNECT] Connecting to C2 server...
[SUCCESS] Connected to C2 server
```

**✨ ¡El nodo aparecerá en tu dashboard automáticamente!**

---

### ✅ Paso 5: Ejecutar Comandos (2 minutos)

En el Dashboard:

1. **Ve a la pestaña "Nodes"**
2. **Haz clic en el nodo** que apareció (punto verde = online)
3. **Ingresa un comando** en el cuadro de texto:

**Ejemplos Windows:**
```
ipconfig
whoami
hostname
systeminfo
```

**Ejemplos Linux/Mac:**
```
ifconfig
whoami
hostname
uname -a
```

4. **Presiona "Execute"**
5. **Ver resultado** en "Command History" (se actualiza en segundos)

---

## 🎯 Comandos de Prueba por Plataforma

### Windows
```cmd
# Información del sistema
systeminfo
ipconfig /all
whoami
hostname

# Procesos y servicios
tasklist
net start
net user

# Red
netstat -an
arp -a
route print

# Directorios
dir C:\
dir C:\Users
```

### Linux/Mac
```bash
# Información del sistema
uname -a
ifconfig -a
whoami
hostname

# Procesos
ps aux
top -n 1

# Red
netstat -tuln
ip addr
ip route

# Directorios
ls -la /home
ls -la /etc
```

---

## 🔥 Funcionalidades del Dashboard

### Tab: Dashboard
- **Total Nodes**: Nodos registrados
- **Online**: Nodos activos
- **Offline**: Nodos desconectados
- **Commands Executed**: Total de comandos ejecutados
- **Recent Activity**: Log de actividad en tiempo real

### Tab: Nodes
- **Lista de nodos**: Ver todos los nodos conectados
- **Seleccionar nodo**: Click para ver detalles
- **Panel de control**: Ejecutar comandos
- **Kill Node**: Eliminar nodo y enviar self-destruct

### Tab: Commands
- **Historial completo** de todos los comandos
- **Estado**: pending, executed, failed
- **Resultados**: Output de cada comando

### Tab: Logs
- **Auditoría completa** de todas las acciones
- Logins, registros, comandos, eliminaciones
- Timestamp y usuario

---

## 🛠️ Gestión de Múltiples Agentes

### Ejecutar en múltiples máquinas

**Máquina 1:**
```bash
python3 /app/agent.py
```

**Máquina 2:**
```bash
python3 /app/agent.py
```

**Máquina 3:**
```bash
python3 /app/agent.py
```

Todos aparecerán en el dashboard y podrás controlarlos individualmente.

---

## 🔄 Ciclo de Vida del Agente

```
┌─────────────────┐
│  Agent Starts   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Registers to   │
│   C2 Server     │ ◄──── Recibe Node ID y Token
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Connects via   │
│   WebSocket     │ ◄──── Cifrado AES-256
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Heartbeat Loop │ ◄──── Cada 30 segundos
│  (Keep-Alive)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Wait for       │
│  Commands       │ ◄──── Ejecuta cuando recibe
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Send Results   │
│  to C2          │
└────────┬────────┘
         │
         │ (Loop continuo hasta kill)
         │
         ▼
┌─────────────────┐
│  Kill Signal    │
│  Received       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Self Destruct  │
│  & Exit         │
└─────────────────┘
```

---

## 🎨 Características Visuales del Dashboard

### Indicadores de Estado
- 🟢 **Verde**: Nodo online
- 🔴 **Rojo**: Nodo offline
- 🟡 **Amarillo**: Pendiente

### Colores de Comandos
- 🟩 **Verde**: Ejecutado exitosamente
- 🟨 **Amarillo**: Pendiente
- 🟥 **Rojo**: Fallido

### Estadísticas en Tiempo Real
- Actualización automática cada 5 segundos
- Sin necesidad de refrescar la página

---

## 🔐 Configuración Rápida de Seguridad

### 1. Cambiar Contraseña Admin

Editar `/app/backend/.env`:
```env
ADMIN_USER="tu_usuario"
ADMIN_PASS="tu_contraseña_segura"
```

Reiniciar:
```bash
sudo supervisorctl restart backend
```

### 2. Generar Nuevas Claves

```bash
cd /app/backend
python3 -c "import secrets; import base64; from Crypto.Random import get_random_bytes; print('SECRET_KEY=' + secrets.token_urlsafe(32)); print('AES_KEY=' + base64.b64encode(get_random_bytes(32)).decode())"
```

Copiar las claves generadas a `/app/backend/.env` y también a `/app/agent.py` (solo AES_KEY).

### 3. Actualizar AES_KEY en Agente

Editar `/app/agent.py` línea 21:
```python
AES_KEY = "tu_nueva_clave_aes_aqui"
```

---

## 🐛 Solución Rápida de Problemas

### Problema: "Cannot connect to C2"

**Solución:**
```bash
# 1. Verificar backend
curl http://localhost:8001/api/

# 2. Si no responde, reiniciar
sudo supervisorctl restart backend

# 3. Ver errores
tail -n 50 /var/log/supervisor/backend.err.log
```

### Problema: "Decryption failed"

**Causa**: AES_KEY no coincide

**Solución:**
```bash
# 1. Verificar clave en backend
grep AES_KEY /app/backend/.env

# 2. Verificar clave en agente
grep AES_KEY /app/agent.py

# 3. Deben ser EXACTAMENTE iguales
```

### Problema: Dashboard no carga

**Solución:**
```bash
# Reiniciar frontend
sudo supervisorctl restart frontend

# Ver estado
sudo supervisorctl status frontend

# Ver logs
tail -f /var/log/supervisor/frontend.err.log
```

---

## 📊 Monitoreo y Logs

### Ver logs en tiempo real

**Backend:**
```bash
tail -f /var/log/supervisor/backend.out.log
```

**Frontend:**
```bash
tail -f /var/log/supervisor/frontend.out.log
```

**Todos:**
```bash
tail -f /var/log/supervisor/*.out.log
```

### Revisar Base de Datos

```bash
mongosh

use c2_framework

# Ver nodos
db.nodes.find().pretty()

# Ver comandos recientes
db.commands.find().sort({timestamp: -1}).limit(10).pretty()

# Ver logs de auditoría
db.audit_logs.find().sort({timestamp: -1}).limit(20).pretty()
```

---

## 🚀 Siguientes Pasos

### Nivel 1: Básico ✅
- [x] Dashboard funcionando
- [x] Agente conectado
- [x] Comandos básicos ejecutándose

### Nivel 2: Intermedio 📖
- [ ] Leer `/app/TUTORIAL_REDTEAM.md` completo
- [ ] Probar comandos avanzados
- [ ] Configurar múltiples agentes
- [ ] Personalizar credenciales

### Nivel 3: Avanzado 🔥
- [ ] Compilar agente a ejecutable (`bash /app/build_agent.sh`)
- [ ] Configurar para red remota
- [ ] Implementar persistencia
- [ ] Añadir módulos personalizados

---

## 📚 Documentación Completa

- **Tutorial Completo**: `/app/TUTORIAL_REDTEAM.md`
- **README**: `/app/README.md`
- **Script de Pruebas**: `/app/test_c2.sh`
- **Build Agent**: `/app/build_agent.sh`

---

## ⚠️ Recuerda

✅ **Solo para uso educativo y autorizado**
✅ **Siempre en entornos controlados**
✅ **Con permisos explícitos por escrito**

❌ **Nunca en sistemas sin autorización**
❌ **Nunca para actividades ilegales**

---

## 🎓 Happy Hacking (Ethical)!

🛡️ **Stay Legal. Stay Ethical. Stay Secure.**

---

**¿Listo para empezar?**

```bash
# 1. Verificar todo
bash /app/test_c2.sh

# 2. Abrir Dashboard
# http://localhost:3000

# 3. Ejecutar Agente
python3 /app/agent.py

# 4. ¡Hackear! (ethically)
```
