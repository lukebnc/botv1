# 🛡️ C2 Framework - Tutorial Completo Red Team

## ⚠️ ADVERTENCIA LEGAL
Este framework es para **USO EDUCATIVO Y AUTORIZADO ÚNICAMENTE**. Solo debe usarse en:
- Entornos de laboratorio controlados
- Sistemas propios con autorización explícita
- Ejercicios de Red Team autorizados por contrato

El uso no autorizado es ILEGAL y puede resultar en acciones legales.

---

## 📋 Índice
1. [Descripción General](#descripción-general)
2. [Características](#características)
3. [Arquitectura](#arquitectura)
4. [Instalación](#instalación)
5. [Configuración](#configuración)
6. [Uso del Framework](#uso-del-framework)
7. [Pruebas en Localhost](#pruebas-en-localhost)
8. [Seguridad](#seguridad)
9. [Troubleshooting](#troubleshooting)

---

## 📖 Descripción General

Framework C2 (Command & Control) profesional con arquitectura P2P diseñado para operaciones de Red Team. Incluye:

- **Backend**: FastAPI con WebSocket para comunicación en tiempo real
- **Frontend**: Dashboard React profesional para gestión de nodos
- **Agente**: Cliente Python con capacidades de ejecución remota
- **Base de datos**: MongoDB para persistencia de datos

---

## ✨ Características

### 🔐 Seguridad
- ✅ Cifrado AES-256 para todas las comunicaciones
- ✅ Autenticación JWT para administradores
- ✅ Tokens únicos por nodo
- ✅ Sistema de kill-switch remoto
- ✅ Logs de auditoría completos
- ✅ Ofuscación de tráfico

### 🎯 Funcionalidades
- ✅ Ejecución remota de comandos
- ✅ Transferencia de archivos (bidireccional)
- ✅ Captura de información del sistema
- ✅ Persistencia y reconexión automática
- ✅ Dashboard en tiempo real
- ✅ Multi-nodo simultáneo
- ✅ Historial de comandos
- ✅ Monitoreo de estado de nodos

### 📊 Dashboard
- Vista en tiempo real de nodos activos
- Estadísticas del sistema
- Panel de comandos interactivo
- Logs de auditoría
- Gestión de nodos

---

## 🏗️ Arquitectura

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Dashboard     │◄────►│   C2 Server     │◄────►│   Agent/Node    │
│   (React)       │      │   (FastAPI)     │      │   (Python)      │
└─────────────────┘      └─────────────────┘      └─────────────────┘
                                 │
                                 ▼
                         ┌─────────────────┐
                         │    MongoDB      │
                         │   (Database)    │
                         └─────────────────┘
```

### Flujo de Comunicación
1. **Agente se registra** → C2 Server asigna ID y token único
2. **Conexión WebSocket** → Comunicación encriptada bidireccional
3. **Heartbeat periódico** → Mantiene conexión activa
4. **Comandos encriptados** → Dashboard → C2 → Agente
5. **Resultados encriptados** → Agente → C2 → Dashboard

---

## 📦 Instalación

### Requisitos Previos
- Python 3.8+
- Node.js 14+
- MongoDB
- pip y yarn

### 1. Backend

```bash
cd /app/backend

# Instalar dependencias
pip install -r requirements.txt

# Las dependencias principales son:
# - fastapi: Framework web
# - websockets: Comunicación en tiempo real
# - pycryptodome: Cifrado AES-256
# - motor: Driver MongoDB asíncrono
# - python-jose: JWT tokens
```

### 2. Frontend

```bash
cd /app/frontend

# Instalar dependencias
yarn install

# Dependencias principales:
# - react: UI framework
# - axios: HTTP client
# - lucide-react: Iconos
# - tailwindcss: Estilos
```

### 3. Agente

```bash
cd /app

# Instalar dependencias del agente
pip install websockets pycryptodome psutil requests

# Dar permisos de ejecución
chmod +x agent.py
```

---

## ⚙️ Configuración

### 1. Variables de Entorno Backend (`/app/backend/.env`)

```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="c2_framework"
CORS_ORIGINS="*"
ADMIN_USER="admin"
ADMIN_PASS="c2admin123"
SECRET_KEY="Smv2MsovvLKvUmEK2uszEmtmixRY0H2Sm9PjvmB4yBA"
AES_KEY="ba4gd0qnveoxHglI4OL8n0jRAteGLexoWN2FbOH2zsU="
```

**IMPORTANTE**: 
- Cambia `ADMIN_USER` y `ADMIN_PASS` en producción
- Las claves `SECRET_KEY` y `AES_KEY` ya están generadas de forma segura
- No compartas estas claves

### 2. Configuración del Agente (`/app/agent.py`)

Edita las líneas 19-23:

```python
C2_SERVER = "ws://localhost:8001/api/ws"
API_SERVER = "http://localhost:8001/api"
AES_KEY = "ba4gd0qnveoxHglI4OL8n0jRAteGLexoWN2FbOH2zsU="
HEARTBEAT_INTERVAL = 30
RECONNECT_DELAY = 5
```

**NOTA**: El `AES_KEY` debe coincidir EXACTAMENTE con el del backend.

### 3. Configuración Frontend

El frontend usa la variable de entorno `REACT_APP_BACKEND_URL` definida en `/app/frontend/.env`:

```env
REACT_APP_BACKEND_URL=https://p2p-botnet-platform.preview.emergentagent.com
```

---

## 🚀 Uso del Framework

### Iniciar el Sistema

#### Opción 1: Usando Supervisor (Recomendado)

```bash
# Iniciar todos los servicios
sudo supervisorctl restart all

# Verificar estado
sudo supervisorctl status

# Ver logs
tail -f /var/log/supervisor/backend.*.log
tail -f /var/log/supervisor/frontend.*.log
```

#### Opción 2: Manual (Para desarrollo)

**Terminal 1 - Backend:**
```bash
cd /app/backend
python3 server.py
# o
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - Frontend:**
```bash
cd /app/frontend
yarn start
```

**Terminal 3 - MongoDB (si no está corriendo):**
```bash
mongod --dbpath /data/db
```

---

## 🧪 Pruebas en Localhost

### Paso 1: Verificar que el Backend está Corriendo

```bash
curl http://localhost:8001/api/
# Respuesta esperada: {"message":"C2 Framework API","status":"operational"}
```

### Paso 2: Acceder al Dashboard

1. Abre navegador: `http://localhost:3000`
2. Credenciales por defecto:
   - **Usuario**: `admin`
   - **Contraseña**: `c2admin123`

### Paso 3: Ejecutar un Agente (Máquina Objetivo)

#### En Windows:

```cmd
# Opción 1: Ejecutar directamente
python agent.py

# Opción 2: En segundo plano
pythonw agent.py
```

#### En Linux/Mac:

```bash
# Opción 1: Ejecutar directamente
python3 agent.py

# Opción 2: En segundo plano
nohup python3 agent.py > /dev/null 2>&1 &
```

### Paso 4: Verificar Conexión en Dashboard

1. Ve a la pestaña **"Nodes"** en el dashboard
2. Deberías ver el nodo conectado con:
   - Estado: **Online** (punto verde)
   - Hostname
   - Sistema operativo
   - Dirección IP

### Paso 5: Ejecutar Comandos

1. **Selecciona el nodo** haciendo clic en él
2. En el panel de comandos, ingresa un comando:

**Ejemplos Windows:**
```
ipconfig
systeminfo
whoami
dir C:\
tasklist
```

**Ejemplos Linux/Mac:**
```
ifconfig
uname -a
whoami
ls -la /home
ps aux
```

3. **Haz clic en "Execute"**
4. Los resultados aparecerán en "Command History"

### Paso 6: Monitorear Actividad

- **Dashboard Tab**: Ver estadísticas globales
- **Logs Tab**: Ver auditoría completa de acciones
- **Commands Tab**: Ver historial de todos los comandos

### Paso 7: Eliminar Nodo (Kill Switch)

1. Selecciona un nodo
2. Haz clic en **"Kill Node"**
3. Confirma la acción
4. El agente se auto-destruirá y desconectará

---

## 🔐 Seguridad

### Cifrado de Comunicaciones

Todas las comunicaciones usan **AES-256 en modo CBC**:

```python
# Estructura del mensaje encriptado
{
  "iv": "base64_encoded_initialization_vector",
  "ciphertext": "base64_encoded_encrypted_data"
}
```

### Autenticación

- **Dashboard**: JWT tokens con expiración de 60 minutos
- **Agentes**: Tokens únicos generados en registro

### Logs de Auditoría

Todas las acciones se registran:
- Logins de administradores
- Registro de nodos
- Ejecución de comandos
- Eliminación de nodos

### Recomendaciones de Seguridad

✅ **HACER:**
- Cambiar contraseñas por defecto
- Usar HTTPS en producción
- Generar nuevas claves para cada deployment
- Mantener logs de auditoría
- Limitar acceso al dashboard por IP
- Usar VPN para comunicaciones C2

❌ **NO HACER:**
- Usar en redes públicas sin VPN
- Compartir tokens o claves
- Ejecutar sin autorización
- Dejar credenciales por defecto

---

## 🧰 Troubleshooting

### Problema: Backend no inicia

```bash
# Verificar MongoDB
sudo systemctl status mongod

# Verificar puerto 8001
netstat -tuln | grep 8001

# Ver logs de error
tail -n 50 /var/log/supervisor/backend.err.log
```

### Problema: Agente no conecta

1. **Verificar que el backend está corriendo**
   ```bash
   curl http://localhost:8001/api/
   ```

2. **Verificar configuración del agente**
   - URLs correctas (C2_SERVER, API_SERVER)
   - AES_KEY coincide con backend

3. **Ver salida del agente**
   ```bash
   python3 agent.py
   # Buscar mensajes de error
   ```

### Problema: Comandos no se ejecutan

1. **Verificar conexión WebSocket**
   - Dashboard muestra nodo como "Online"

2. **Revisar logs del agente**
   - Debe mostrar "[COMMAND] Executing: ..."

3. **Verificar permisos**
   - El usuario que ejecuta el agente tiene permisos para el comando

### Problema: Frontend no carga

```bash
# Verificar instalación
cd /app/frontend
yarn install

# Verificar .env
cat .env
# Debe tener REACT_APP_BACKEND_URL

# Reiniciar
sudo supervisorctl restart frontend
```

---

## 📊 Estructura de Base de Datos

### Colección: `nodes`
```json
{
  "id": "uuid",
  "hostname": "string",
  "os": "string",
  "ip": "string",
  "status": "online|offline",
  "token": "unique_token",
  "last_seen": "ISO datetime",
  "created_at": "ISO datetime",
  "cpu_usage": "float",
  "memory_usage": "float",
  "disk_usage": "float"
}
```

### Colección: `commands`
```json
{
  "id": "uuid",
  "node_id": "uuid",
  "command": "string",
  "result": "string",
  "status": "pending|executed|failed",
  "timestamp": "ISO datetime"
}
```

### Colección: `audit_logs`
```json
{
  "id": "uuid",
  "action": "string",
  "user": "string",
  "node_id": "uuid",
  "details": "string",
  "timestamp": "ISO datetime"
}
```

---

## 🎯 Casos de Uso Red Team

### 1. Reconocimiento
```bash
# Información del sistema
systeminfo          # Windows
uname -a           # Linux

# Información de red
ipconfig /all      # Windows
ifconfig -a        # Linux
netstat -an        # Ambos

# Usuarios
net user           # Windows
cat /etc/passwd    # Linux
```

### 2. Enumeración
```bash
# Procesos en ejecución
tasklist           # Windows
ps aux             # Linux

# Servicios
net start          # Windows
systemctl list-units --type=service  # Linux

# Conexiones de red
netstat -ano       # Windows
ss -tunap          # Linux
```

### 3. Persistence (Solo en entornos autorizados)
```bash
# Verificar tareas programadas
schtasks /query    # Windows
crontab -l         # Linux
```

---

## 🔧 Personalización

### Agregar Nuevos Comandos Especiales

Edita `/app/backend/server.py` en la función `handle_message`:

```python
elif msg_type == 'custom_command':
    # Tu lógica personalizada aquí
    pass
```

### Agregar Transferencia de Archivos

Implementa endpoints en backend:
```python
@api_router.post("/upload")
async def upload_file():
    # Lógica de subida
    pass

@api_router.get("/download/{file_id}")
async def download_file():
    # Lógica de descarga
    pass
```

---

## 📝 Notas Finales

### Limitaciones Conocidas
- El agente requiere Python instalado en la máquina objetivo
- Las comunicaciones WebSocket pueden ser detectadas por firewalls avanzados
- El cifrado protege el contenido pero no oculta el tráfico

### Mejoras Futuras
- [ ] Compilar agente a binario (PyInstaller)
- [ ] Implementar C2 sobre HTTP/HTTPS (stealth)
- [ ] Agregar transferencia de archivos
- [ ] Implementar keylogger módulo
- [ ] Screenshot remoto
- [ ] Soporte multi-plataforma mejorado
- [ ] Persistencia automática

### Recursos Adicionales
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [Red Team Notes](https://www.ired.team/)
- [Cobalt Strike Documentation](https://www.cobaltstrike.com/help)

---

## ⚖️ Disclaimer Legal

Este software se proporciona "tal cual" para fines educativos y de investigación de seguridad únicamente. Los desarrolladores no son responsables del uso indebido o daños causados por este software. El usuario es el único responsable de cumplir con todas las leyes y regulaciones aplicables.

**EL USO NO AUTORIZADO DE ESTE SOFTWARE ES ILEGAL Y PUEDE RESULTAR EN SANCIONES PENALES.**

---

## 📞 Soporte

Para problemas técnicos o preguntas:
1. Revisar esta documentación completa
2. Verificar logs del sistema
3. Consultar troubleshooting section

---

**Desarrollado para fines educativos y de Red Team autorizado**

🛡️ **Stay Legal. Stay Ethical. Stay Secure.**
