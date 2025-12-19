# 📁 Estructura Completa del Proyecto

```
/app/
│
├── 📄 README.md                    # Documentación principal
├── 📄 TUTORIAL_REDTEAM.md         # Tutorial completo (LEER PRIMERO)
├── 📄 QUICKSTART.md               # Guía de inicio rápido
├── 📄 FAQ.md                      # Preguntas frecuentes
├── 📄 REDTEAM_COMMANDS.md         # Referencia de comandos
├── 📄 PROJECT_STRUCTURE.md        # Este archivo
│
├── 🐍 agent.py                    # Agente/Payload principal
├── 🔧 test_c2.sh                  # Script de pruebas automáticas
├── 🔧 build_agent.sh              # Script para compilar agente
│
├── 📂 backend/                    # Servidor C2 Backend
│   ├── server.py                  # Aplicación FastAPI principal
│   ├── requirements.txt           # Dependencias Python
│   └── .env                       # Configuración y claves
│
├── 📂 frontend/                   # Dashboard Web Frontend
│   ├── public/                    # Archivos estáticos
│   ├── src/
│   │   ├── App.js                 # Componente principal React
│   │   ├── App.css                # Estilos principales
│   │   ├── index.js               # Punto de entrada
│   │   └── index.css              # Estilos globales
│   ├── package.json               # Dependencias Node.js
│   ├── tailwind.config.js         # Configuración Tailwind
│   └── .env                       # Variables de entorno
│
├── 📂 tests/                      # Directorio de tests
│   └── __init__.py
│
└── 📂 build/                      # Binarios compilados (generado)
    └── c2_agent                   # Agente ejecutable
```

## 🔑 Archivos Clave

### Backend - server.py
**Propósito**: Servidor C2 principal
**Contiene**:
- Endpoints API REST
- WebSocket server para agentes
- Gestión de nodos y comandos
- Sistema de autenticación JWT
- Cifrado AES-256
- Logs de auditoría

**Endpoints principales**:
```
POST   /api/auth/login          # Autenticación
GET    /api/nodes               # Listar nodos
POST   /api/nodes/register      # Registrar nodo
DELETE /api/nodes/{id}          # Eliminar nodo (kill)
POST   /api/commands            # Ejecutar comando
GET    /api/commands            # Historial
GET    /api/stats               # Estadísticas
GET    /api/logs                # Auditoría
WS     /api/ws/{token}          # WebSocket agentes
```

### Frontend - App.js
**Propósito**: Dashboard de control
**Contiene**:
- Login de administrador
- Vista de nodos activos
- Panel de ejecución de comandos
- Historial de comandos
- Logs de auditoría
- Estadísticas en tiempo real

**Tabs**:
- Dashboard: Resumen y estadísticas
- Nodes: Gestión de nodos
- Commands: Historial completo
- Logs: Auditoría del sistema

### Agente - agent.py
**Propósito**: Cliente que se ejecuta en máquinas objetivo
**Contiene**:
- Registro automático con C2
- Conexión WebSocket persistente
- Ejecución de comandos del sistema
- Heartbeat (keep-alive)
- Cifrado de comunicaciones
- Reconexión automática
- Self-destruct (kill switch)

**Características**:
- Multi-plataforma (Windows, Linux, Mac)
- Compilable a binario
- Ofuscación de tráfico
- Captura de info del sistema

### Configuración - .env files

#### Backend .env
```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="c2_framework"
CORS_ORIGINS="*"
ADMIN_USER="admin"
ADMIN_PASS="c2admin123"
SECRET_KEY="<JWT secret>"
AES_KEY="<AES-256 key base64>"
```

#### Frontend .env
```env
REACT_APP_BACKEND_URL=<URL del backend>
WDS_SOCKET_PORT=443
ENABLE_HEALTH_CHECK=false
```

## 📊 Base de Datos MongoDB

### Estructura

```
c2_framework (database)
├── nodes (collection)
│   ├── id (string, UUID)
│   ├── hostname (string)
│   ├── os (string)
│   ├── ip (string)
│   ├── status (string: online/offline)
│   ├── token (string, unique)
│   ├── last_seen (datetime)
│   ├── created_at (datetime)
│   └── cpu_usage, memory_usage, disk_usage (float)
│
├── commands (collection)
│   ├── id (string, UUID)
│   ├── node_id (string, ref: nodes.id)
│   ├── command (string)
│   ├── result (string)
│   ├── status (string: pending/executed/failed)
│   └── timestamp (datetime)
│
└── audit_logs (collection)
    ├── id (string, UUID)
    ├── action (string)
    ├── user (string)
    ├── node_id (string, optional)
    ├── details (string)
    └── timestamp (datetime)
```

## 🔄 Flujo de Datos

### Registro de Nodo
```
1. Agent.py se ejecuta
2. Recopila info del sistema
3. POST /api/nodes/register
4. Recibe: node_id, token
5. Conecta vía WebSocket
```

### Ejecución de Comando
```
1. Admin ingresa comando en Dashboard
2. POST /api/commands {node_id, command}
3. Backend envía via WebSocket (encriptado)
4. Agent ejecuta comando
5. Agent envía resultado (encriptado)
6. Backend actualiza DB
7. Dashboard muestra resultado
```

### Heartbeat
```
1. Agent envía heartbeat cada 30s
2. Incluye info del sistema
3. Backend actualiza last_seen
4. Dashboard refleja estado online
```

## 🛠️ Dependencias

### Backend (Python)
```
fastapi==0.110.1           # Web framework
uvicorn==0.25.0            # ASGI server
motor==3.3.1               # MongoDB async driver
pydantic>=2.6.4            # Data validation
python-jose>=3.3.0         # JWT tokens
pycryptodome               # AES encryption
websockets                 # WebSocket support
```

### Frontend (Node.js)
```
react@19.0.0               # UI framework
react-dom@19.0.0           # React DOM
axios@1.8.4                # HTTP client
tailwindcss@3.4.17         # CSS framework
lucide-react@0.507.0       # Icons
```

### Agente (Python)
```
websockets                 # WebSocket client
pycryptodome              # AES encryption
psutil                    # System info
requests                  # HTTP client
```

## 📝 Scripts Útiles

### test_c2.sh
Ejecuta tests de todos los componentes:
- Backend health check
- MongoDB status
- Frontend accessibility
- Authentication test
- Node registration
- API endpoints
- Statistics

Uso:
```bash
bash /app/test_c2.sh
```

### build_agent.sh
Compila el agente a ejecutable standalone:
- Usa PyInstaller
- Genera binario en /app/build/
- Incluye todas las dependencias
- ~15-20 MB de tamaño

Uso:
```bash
bash /app/build_agent.sh
```

## 🗂️ Logs

### Ubicaciones
```
/var/log/supervisor/backend.out.log      # Backend stdout
/var/log/supervisor/backend.err.log      # Backend stderr
/var/log/supervisor/frontend.out.log     # Frontend stdout
/var/log/supervisor/frontend.err.log     # Frontend stderr
/var/log/supervisor/mongodb.out.log      # MongoDB stdout
```

### Ver logs en tiempo real
```bash
tail -f /var/log/supervisor/backend.out.log
tail -f /var/log/supervisor/*.out.log    # Todos
```

## 🔐 Seguridad

### Cifrado
- **Algoritmo**: AES-256 CBC
- **Key Length**: 256 bits (32 bytes)
- **IV**: Generado aleatoriamente por mensaje
- **Encoding**: Base64

### Autenticación
- **Admin**: JWT tokens (HS256)
- **Agentes**: Tokens únicos por nodo
- **Expiración**: 60 minutos (JWT)

### Comunicación
```
Dashboard ←→ Backend: HTTPS (en producción)
Backend ←→ Agent: WebSocket (cifrado AES-256)
```

## 🚀 Despliegue

### Local (Desarrollo)
```bash
sudo supervisorctl restart all
```

### Producción (Recomendaciones)
1. **Usar HTTPS/WSS**
2. **Reverse proxy** (nginx)
3. **Firewall** configurado
4. **VPN** para acceso
5. **Monitoreo** activo
6. **Backups** regulares
7. **Logs** centralizados

## 📚 Documentación

### Para Usuarios Finales
1. **README.md**: Overview general
2. **QUICKSTART.md**: Inicio rápido en 5 minutos
3. **FAQ.md**: Preguntas frecuentes

### Para Red Team
1. **TUTORIAL_REDTEAM.md**: Tutorial completo
2. **REDTEAM_COMMANDS.md**: Referencia de comandos
3. **FAQ.md**: Troubleshooting avanzado

### Para Desarrolladores
1. **PROJECT_STRUCTURE.md**: Este archivo
2. Comentarios en código fuente
3. API documentation (inline)

## 🎯 Extensiones Posibles

### Backend
- [ ] Transferencia de archivos
- [ ] Screenshot remoto
- [ ] Keylogger módulo
- [ ] Privilege escalation helpers
- [ ] Multi-user support
- [ ] Role-based access

### Frontend
- [ ] File browser interface
- [ ] Real-time terminal
- [ ] Screenshot viewer
- [ ] Network graph visualization
- [ ] Export reports (PDF)

### Agente
- [ ] Auto-update capability
- [ ] Plugin system
- [ ] More evasion techniques
- [ ] Cross-compilation support
- [ ] Custom protocols (DNS, ICMP)

## 🔗 Integración con Otras Herramientas

### Recomendadas
- **Metasploit**: Para exploits
- **BloodHound**: Para AD enumeration
- **Nmap**: Para network scanning
- **Burp Suite**: Para web testing

### Posibles Integraciones
- API webhooks
- Syslog forwarding
- SIEM integration
- Threat intelligence feeds

## 📞 Comandos de Mantenimiento

### Reiniciar servicios
```bash
sudo supervisorctl restart backend
sudo supervisorctl restart frontend
sudo supervisorctl restart mongodb
sudo supervisorctl restart all
```

### Ver estado
```bash
sudo supervisorctl status
```

### Limpiar base de datos
```bash
mongosh
use c2_framework
db.nodes.deleteMany({})
db.commands.deleteMany({})
db.audit_logs.deleteMany({})
```

### Backup
```bash
# Base de datos
mongodump --db c2_framework --out /backup/c2_$(date +%Y%m%d)

# Código
tar -czf /backup/c2_code_$(date +%Y%m%d).tar.gz /app
```

### Restore
```bash
mongorestore --db c2_framework /backup/c2_YYYYMMDD/c2_framework
```

---

**Estructura creada para uso educativo y profesional en Red Team**

🛡️ **Stay Legal. Stay Ethical. Stay Secure.**
