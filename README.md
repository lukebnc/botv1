# 🛡️ C2 Framework - Red Team Professional

## ⚠️ ADVERTENCIA LEGAL
**Solo para uso educativo y en entornos autorizados. El uso no autorizado es ILEGAL.**

---

## 🚀 Inicio Rápido

### 1. Verificar que todo está corriendo
```bash
sudo supervisorctl status
```

### 2. Acceder al Dashboard
- URL: `http://localhost:3000`
- Usuario: `admin`
- Contraseña: `c2admin123`

### 3. Ejecutar un Agente (máquina objetivo)
```bash
python3 /app/agent.py
```

### 4. Gestionar Nodos
1. Ve a la pestaña **"Nodes"** en el dashboard
2. Selecciona un nodo conectado
3. Ejecuta comandos en el panel de control

---

## 📊 Características Principales

### ✅ Seguridad Avanzada
- Cifrado AES-256 en todas las comunicaciones
- Autenticación JWT para administradores
- Tokens únicos por nodo
- Kill-switch remoto
- Logs de auditoría completos

### ✅ Funcionalidades Básicas
- Ejecución remota de comandos
- Monitoreo de nodos en tiempo real
- Dashboard profesional React
- WebSocket para comunicación P2P
- Reconexión automática de agentes
- Captura de información del sistema

### 🔥 Funcionalidades AVANZADAS (Nuevas!)
- 📸 **Screenshot Capture** - Captura de pantalla remota en tiempo real
- 📁 **File Browser** - Navegador de archivos con descarga/upload
- ⌨️ **Keylogger** - Captura de pulsaciones de teclado
- 🍪 **Cookie Stealer** - Extracción de cookies de navegadores
- 🔨 **Payload Builder** - Generador de .exe desde el dashboard

### ✅ Panel de Control
- Vista de nodos activos/inactivos
- Estadísticas en tiempo real
- Historial de comandos
- Logs de auditoría
- Gestión multi-nodo
- **Tab Advanced** - Acceso a funcionalidades RAT
- **Tab Builder** - Generador de payloads personalizados

---

## 🏗️ Arquitectura

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Dashboard  │ ◄─────► │  C2 Server   │ ◄─────► │    Agent     │
│   (React)    │  HTTPS  │  (FastAPI)   │   WSS   │  (Python)    │
└──────────────┘         └──────────────┘         └──────────────┘
                               │
                               ▼
                         ┌──────────────┐
                         │   MongoDB    │
                         └──────────────┘
```

---

## 📂 Estructura del Proyecto

```
/app/
├── backend/
│   ├── server.py           # Servidor C2 principal
│   ├── requirements.txt    # Dependencias Python
│   └── .env               # Configuración (claves, credenciales)
│
├── frontend/
│   ├── src/
│   │   ├── App.js         # Dashboard React
│   │   └── App.css        # Estilos
│   ├── package.json       # Dependencias Node
│   └── .env              # URL del backend
│
├── agent.py               # Agente/Payload para nodos
├── test_c2.sh            # Script de prueba automática
├── TUTORIAL_REDTEAM.md   # Tutorial completo (LEER PRIMERO)
└── README.md             # Este archivo
```

---

## 🧪 Pruebas Rápidas

### Opción 1: Script Automático
```bash
bash /app/test_c2.sh
```

### Opción 2: Manual

**Verificar Backend:**
```bash
curl http://localhost:8001/api/
```

**Verificar Autenticación:**
```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"c2admin123"}'
```

**Registrar un Nodo de Prueba:**
```bash
curl -X POST http://localhost:8001/api/nodes/register \
  -H "Content-Type: application/json" \
  -d '{"hostname":"test","os":"Linux","ip":"127.0.0.1"}'
```

---

## 🔧 Comandos Útiles

### Gestión de Servicios
```bash
# Reiniciar todo
sudo supervisorctl restart all

# Ver estado
sudo supervisorctl status

# Ver logs
tail -f /var/log/supervisor/backend.*.log
tail -f /var/log/supervisor/frontend.*.log
```

### Ejecutar Agente
```bash
# Modo normal (ver output)
python3 /app/agent.py

# Modo background
nohup python3 /app/agent.py > /dev/null 2>&1 &
```

### Base de Datos
```bash
# Conectar a MongoDB
mongosh

# Ver bases de datos
show dbs

# Usar base de datos C2
use c2_framework

# Ver colecciones
show collections

# Ver nodos
db.nodes.find()

# Ver comandos
db.commands.find()

# Ver logs
db.audit_logs.find()
```

---

## 📖 Documentación Completa

Para el tutorial completo con:
- Configuración detallada
- Casos de uso Red Team
- Troubleshooting
- Personalización
- Seguridad avanzada

**Lee el archivo:** `/app/TUTORIAL_REDTEAM.md`

```bash
cat /app/TUTORIAL_REDTEAM.md
# o
less /app/TUTORIAL_REDTEAM.md
```

---

## 🎯 Casos de Uso Rápidos

### Reconocimiento Básico

**Windows:**
```
ipconfig
systeminfo
whoami
hostname
```

**Linux:**
```
ifconfig
uname -a
whoami
hostname
```

### Información de Red
```
netstat -an          # Conexiones activas
arp -a              # Tabla ARP
route print         # Tabla de rutas (Windows)
ip route           # Tabla de rutas (Linux)
```

### Procesos y Servicios
```
tasklist           # Windows
ps aux            # Linux
```

---

## 🔐 Seguridad

### Credenciales por Defecto
- **Usuario**: `admin`
- **Contraseña**: `c2admin123`

⚠️ **CAMBIAR EN PRODUCCIÓN** editando `/app/backend/.env`

### Claves de Cifrado
Las claves AES-256 y JWT están en `/app/backend/.env`:
```env
SECRET_KEY="Smv2MsovvLKvUmEK2uszEmtmixRY0H2Sm9PjvmB4yBA"
AES_KEY="ba4gd0qnveoxHglI4OL8n0jRAteGLexoWN2FbOH2zsU="
```

⚠️ **NO COMPARTIR ESTAS CLAVES**

### Agente
El agente debe tener la misma `AES_KEY` que el servidor.
Verifica línea 21 de `/app/agent.py`

---

## 🐛 Troubleshooting

### Backend no inicia
```bash
# Ver errores
tail -n 50 /var/log/supervisor/backend.err.log

# Verificar MongoDB
sudo systemctl status mongod

# Reiniciar
sudo supervisorctl restart backend
```

### Agente no conecta
1. Verifica que backend esté corriendo: `curl http://localhost:8001/api/`
2. Verifica la `AES_KEY` en `/app/agent.py`
3. Ejecuta agente con: `python3 /app/agent.py` (ver errores)

### Frontend no carga
```bash
# Verificar estado
sudo supervisorctl status frontend

# Ver logs
tail -f /var/log/supervisor/frontend.*.log

# Reiniciar
sudo supervisorctl restart frontend
```

---

## 📊 Endpoints API

### Autenticación
- `POST /api/auth/login` - Login de administrador

### Nodos
- `GET /api/nodes` - Listar todos los nodos
- `GET /api/nodes/{id}` - Obtener nodo específico
- `POST /api/nodes/register` - Registrar nuevo nodo
- `DELETE /api/nodes/{id}` - Eliminar nodo (kill)

### Comandos
- `POST /api/commands` - Ejecutar comando en nodo
- `GET /api/commands` - Listar comandos
- `POST /api/commands/result` - Enviar resultado (agente)

### Estadísticas
- `GET /api/stats` - Estadísticas globales
- `GET /api/logs` - Logs de auditoría

### WebSocket
- `WS /api/ws/{token}` - Conexión agente

---

## 🎓 Aprendizaje

Este framework es una implementación educativa completa de:
- Arquitectura C2 moderna
- Comunicación encriptada P2P
- Gestión de agentes distribuidos
- Dashboard de control profesional
- Seguridad en Red Team

### Recursos Recomendados
- [MITRE ATT&CK](https://attack.mitre.org/)
- [Red Team Notes](https://www.ired.team/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

---

## 📝 Notas Importantes

### ✅ Usar Para:
- Educación en seguridad ofensiva
- Ejercicios de Red Team autorizados
- Investigación de seguridad
- Laboratorios controlados

### ❌ NO Usar Para:
- Acceso no autorizado
- Actividades ilegales
- Sistemas sin permiso explícito
- Entornos de producción sin autorización

---

## ⚖️ Disclaimer

Este software es para **FINES EDUCATIVOS Y AUTORIZADOS ÚNICAMENTE**.

Los desarrolladores no son responsables del uso indebido. El usuario es el único responsable de cumplir con todas las leyes aplicables.

**EL USO NO AUTORIZADO ES ILEGAL.**

---

## 🤝 Contribuir

Este es un proyecto educativo. Para mejoras:
1. Revisa el código en `/app/backend/server.py`
2. Mejora funcionalidades existentes
3. Añade características de seguridad
4. Documenta tus cambios

---

## 📞 Soporte

1. **Leer primero**: `/app/TUTORIAL_REDTEAM.md`
2. **Revisar logs**: `/var/log/supervisor/`
3. **Script de test**: `bash /app/test_c2.sh`

---

**Desarrollado para Red Team Profesional**

🛡️ **Stay Legal. Stay Ethical. Stay Secure.**

---

## 📄 Licencia

Educational Use Only - Use at your own risk
