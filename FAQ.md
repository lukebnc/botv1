# ❓ FAQ - Preguntas Frecuentes

## 📋 General

### ¿Qué es este framework?
Es un sistema Command & Control (C2) profesional diseñado para operaciones de Red Team en entornos autorizados. Permite controlar remotamente múltiples nodos mediante una interfaz web.

### ¿Es legal usar esto?
**Solo es legal en:**
- Sistemas propios
- Entornos de prueba autorizados
- Ejercicios de Red Team con contrato
- Educación en entornos controlados

**Es ILEGAL usarlo sin autorización explícita.**

### ¿Qué tecnologías usa?
- **Backend**: Python + FastAPI + WebSocket
- **Frontend**: React + TailwindCSS
- **Database**: MongoDB
- **Security**: AES-256 + JWT
- **Agent**: Python (compilable a binario)

---

## 🚀 Instalación y Configuración

### ¿Cómo inicio el sistema?
```bash
sudo supervisorctl restart all
```

### ¿Cómo verifico que todo está funcionando?
```bash
bash /app/test_c2.sh
```

### ¿Dónde están las credenciales?
**Dashboard:**
- Usuario: `admin`
- Contraseña: `c2admin123`

Cambiar en: `/app/backend/.env`

### ¿Cómo cambio las contraseñas?
1. Editar `/app/backend/.env`:
   ```env
   ADMIN_USER="nuevo_usuario"
   ADMIN_PASS="nueva_contraseña"
   ```
2. Reiniciar: `sudo supervisorctl restart backend`

### ¿Cómo genero nuevas claves de cifrado?
```bash
cd /app/backend
python3 -c "import secrets; import base64; from Crypto.Random import get_random_bytes; print('SECRET_KEY=' + secrets.token_urlsafe(32)); print('AES_KEY=' + base64.b64encode(get_random_bytes(32)).decode())"
```

Copiar el resultado a `/app/backend/.env` y la `AES_KEY` también a `/app/agent.py`.

---

## 🔧 Uso del Framework

### ¿Cómo accedo al dashboard?
1. Abrir navegador: http://localhost:3000
2. Login con credenciales
3. Navegar por las pestañas

### ¿Cómo ejecuto un agente?
```bash
python3 /app/agent.py
```

El agente se registrará automáticamente y aparecerá en el dashboard.

### ¿Cómo ejecuto comandos?
1. Ve a la pestaña "Nodes"
2. Selecciona un nodo (click)
3. Escribe el comando en el campo de texto
4. Presiona "Execute"
5. Los resultados aparecen en "Command History"

### ¿Puedo controlar múltiples nodos?
Sí, puedes tener tantos nodos como necesites conectados simultáneamente. Cada uno se controla individualmente desde el dashboard.

### ¿Cómo elimino un nodo?
1. Selecciona el nodo
2. Click en "Kill Node"
3. Confirma la acción
4. El agente recibirá señal de self-destruct

---

## 🌐 Red y Conectividad

### ¿El agente funciona en otra máquina?
Sí, pero debes cambiar las URLs en `/app/agent.py`:

```python
C2_SERVER = "ws://IP_DEL_SERVIDOR:8001/api/ws"
API_SERVER = "http://IP_DEL_SERVIDOR:8001/api"
```

### ¿Funciona a través de Internet?
Sí, pero requiere:
1. Puerto 8001 expuesto (backend)
2. Puerto 3000 expuesto (frontend)
3. Configurar URLs públicas
4. Usar HTTPS/WSS en producción
5. Configurar firewall adecuadamente

**Recomendación**: Usar VPN para seguridad adicional.

### ¿Puedo usar HTTPS?
Sí, necesitas:
1. Certificado SSL
2. Configurar nginx/reverse proxy
3. Actualizar URLs en frontend (.env)
4. Cambiar `ws://` por `wss://` en agente

### ¿El tráfico está cifrado?
Sí, todas las comunicaciones usan:
- **AES-256** en modo CBC
- **JWT** para autenticación de admin
- **Tokens únicos** por nodo

---

## 🐛 Troubleshooting

### El backend no inicia
**Causa común**: MongoDB no está corriendo

**Solución**:
```bash
sudo systemctl start mongod
sudo supervisorctl restart backend
```

**Ver errores**:
```bash
tail -n 50 /var/log/supervisor/backend.err.log
```

### El agente no conecta
**Posibles causas**:

1. **Backend no está corriendo**
   ```bash
   curl http://localhost:8001/api/
   ```

2. **AES_KEY no coincide**
   ```bash
   grep AES_KEY /app/backend/.env
   grep AES_KEY /app/agent.py
   # Deben ser iguales
   ```

3. **URL incorrecta en agente**
   - Verificar líneas 19-20 de `/app/agent.py`

### Los comandos no se ejecutan
**Verificar**:

1. **Nodo está online** (punto verde en dashboard)
2. **WebSocket conectado** (ver logs del agente)
3. **Permisos del comando** (el usuario del agente tiene permisos)

**Ver logs del agente**:
```bash
python3 /app/agent.py
# Debe mostrar: [COMMAND] Executing: ...
```

### Frontend muestra error
**Solución**:
```bash
# Reiniciar frontend
sudo supervisorctl restart frontend

# Ver logs
tail -f /var/log/supervisor/frontend.err.log

# Si persiste, reinstalar dependencias
cd /app/frontend
yarn install
sudo supervisorctl restart frontend
```

### "Authentication failed"
**Causas**:

1. **Credenciales incorrectas**
   - Verificar en `/app/backend/.env`

2. **Token expirado**
   - Hacer logout y login nuevamente

3. **Backend reiniciado**
   - Hacer logout y login nuevamente

### Base de datos no funciona
```bash
# Verificar MongoDB
sudo systemctl status mongod

# Iniciar si está parado
sudo systemctl start mongod

# Verificar conexión
mongosh
# Debe conectar sin error
```

---

## 🔐 Seguridad

### ¿Es seguro usar esto?
El framework implementa buenas prácticas de seguridad:
- Cifrado AES-256
- Autenticación JWT
- Tokens únicos por nodo
- Logs de auditoría

**Pero**: Úsalo solo en entornos controlados y autorizados.

### ¿Puede ser detectado?
Sí, especialmente por:
- EDR/Antivirus modernos
- IDS/IPS
- Firewalls de aplicación
- Monitoreo de red

**Para evasión**: Requiere técnicas avanzadas de ofuscación.

### ¿Deja rastros?
Sí:
- Logs del sistema operativo
- Logs de red
- Procesos en ejecución
- Conexiones de red
- Logs de auditoría en la base de datos

**Importante**: En ejercicios reales, documenta todo.

### ¿Cómo protejo mi C2 server?
1. **Cambiar credenciales** por defecto
2. **Generar nuevas claves** de cifrado
3. **Usar firewall** (solo IPs autorizadas)
4. **Usar VPN** para acceso
5. **Monitorear logs** constantemente
6. **Actualizar** regularmente
7. **Limitar acceso** al dashboard

---

## 💻 Desarrollo y Personalización

### ¿Puedo compilar el agente?
Sí:
```bash
bash /app/build_agent.sh
```

Genera un ejecutable standalone en `/app/build/c2_agent`.

### ¿Puedo añadir funcionalidades?
Sí, el código es completamente modificable:

**Backend**: `/app/backend/server.py`
**Frontend**: `/app/frontend/src/App.js`
**Agente**: `/app/agent.py`

### ¿Cómo añado transferencia de archivos?
Necesitas implementar:

1. **Backend**: Endpoints de upload/download
2. **Agente**: Funciones de read/write files
3. **Frontend**: UI para gestionar archivos

Ver comentarios en el código para guía.

### ¿Puedo cambiar el puerto?
Sí, pero mantén consistencia:

**Backend** (no recomendado cambiar):
- Supervisor controla el puerto 8001
- Si cambias, actualiza supervisord.conf

**Frontend**: Puerto 3000 (gestionado por React)

### ¿Soporta Windows como target?
Sí, el agente funciona en Windows, Linux y Mac.

**Requiere**:
- Python 3.8+ instalado
- Dependencias: `pip install websockets pycryptodome psutil requests`

### ¿Puedo usar otro lenguaje para el agente?
Sí, solo necesitas:
1. Implementar el protocolo de comunicación
2. Cifrado AES-256 compatible
3. WebSocket client
4. Ejecución de comandos del sistema

---

## 📊 Base de Datos

### ¿Cómo accedo a la base de datos?
```bash
mongosh
use c2_framework
```

### ¿Qué colecciones hay?
- `nodes`: Información de nodos
- `commands`: Historial de comandos
- `audit_logs`: Logs de auditoría

### ¿Cómo borro todos los datos?
```bash
mongosh
use c2_framework
db.nodes.deleteMany({})
db.commands.deleteMany({})
db.audit_logs.deleteMany({})
```

### ¿Cómo hago backup?
```bash
mongodump --db c2_framework --out /backup/c2_backup
```

### ¿Cómo restauro un backup?
```bash
mongorestore --db c2_framework /backup/c2_backup/c2_framework
```

---

## 🎯 Casos de Uso

### ¿Para qué sirve esto?
**Legítimo**:
- Educación en seguridad ofensiva
- Ejercicios de Red Team autorizados
- Simulación de adversarios
- Pruebas de seguridad
- Investigación académica

**Ilegal** (NO HACER):
- Acceso no autorizado
- Malware
- Ataques reales
- Espionaje

### ¿Qué comandos puedo ejecutar?
Cualquier comando del sistema operativo que el usuario del agente tenga permisos para ejecutar.

Ver: `/app/REDTEAM_COMMANDS.md` para referencia completa.

### ¿Puedo hacer pentesting con esto?
Solo si:
1. Tienes autorización **por escrito**
2. Está dentro del scope del engagement
3. El cliente está informado
4. Respetas las reglas de engagement

---

## 📚 Recursos y Aprendizaje

### ¿Dónde aprendo más sobre C2?
- [MITRE ATT&CK](https://attack.mitre.org/)
- [Red Team Notes](https://www.ired.team/)
- [Cobalt Strike Documentation](https://www.cobaltstrike.com/help)
- [Empire C2](https://github.com/BC-SECURITY/Empire)

### ¿Qué otros frameworks C2 existen?
- Cobalt Strike (comercial)
- Metasploit Framework
- Empire
- Covenant
- Sliver
- PoshC2

### ¿Cómo mejoro mis habilidades de Red Team?
1. **Certificaciones**: OSCP, CRTO, PNPT
2. **Práctica**: HackTheBox, TryHackMe
3. **Libros**: "Red Team Field Manual"
4. **Labs**: Crear entornos de prueba
5. **CTFs**: Participar en competencias

---

## 🆘 Soporte

### ¿Dónde obtengo ayuda?
1. **Leer documentación**:
   - `/app/README.md`
   - `/app/TUTORIAL_REDTEAM.md`
   - `/app/QUICKSTART.md`

2. **Revisar logs**:
   ```bash
   tail -f /var/log/supervisor/*.log
   ```

3. **Ejecutar tests**:
   ```bash
   bash /app/test_c2.sh
   ```

### ¿Cómo reporto un bug?
Este es un proyecto educativo. Para bugs:
1. Verifica que no sea un error de configuración
2. Revisa los logs completos
3. Documenta los pasos para reproducir

### ¿Hay una comunidad?
Este es un proyecto educacional standalone. Para aprendizaje de Red Team, únete a:
- r/netsec (Reddit)
- r/AskNetsec (Reddit)
- Discord servers de seguridad
- Foros de HackTheBox

---

## ⚖️ Legal y Ético

### ¿Puedo usar esto en mi trabajo?
Solo si:
1. Tu empresa lo autoriza explícitamente
2. Es parte de un engagement autorizado
3. Está en el scope del proyecto
4. Tienes permiso por escrito

### ¿Qué pasa si lo uso mal?
**Consecuencias legales**:
- Cargos criminales
- Multas
- Prisión
- Pérdida de empleo
- Prohibición de trabajar en tecnología

**NO vale la pena el riesgo.**

### ¿Es ético hacer Red Team?
Sí, cuando:
- Tienes autorización
- Mejoras la seguridad
- Reportas responsablemente
- No causas daño innecesario
- Respetas la privacidad

---

## 🔄 Actualizaciones

### ¿Cómo actualizo el framework?
Si haces cambios:
1. **Backup** de la base de datos
2. **Documentar** cambios
3. **Probar** en entorno de desarrollo
4. **Desplegar** gradualmente

### ¿Hay nueva versión?
Este es un proyecto educativo standalone. Para mejorar:
1. Revisa el código
2. Implementa nuevas features
3. Comparte conocimiento

---

## 💡 Tips y Trucos

### Performance

**Optimizar conexiones**:
- Ajustar `HEARTBEAT_INTERVAL` en agente (línea 22)
- Reducir frecuencia de actualización en dashboard

**Múltiples nodos**:
- MongoDB puede manejar miles de nodos
- Backend escala con más recursos
- Considera load balancer para muchos nodos

### Seguridad Adicional

**Ofuscación básica**:
- Compilar agente a binario
- Cambiar nombres de variables
- Usar packers/crypters (educational)

**Network stealth**:
- Usar dominios legítimos
- Implementar domain fronting
- Agregar jitter a heartbeats

**Evasión básica**:
- Sleep antes de conectar
- Randomizar User-Agent
- Implementar check de VM/sandbox

---

## 🎓 Escenarios de Práctica

### Lab Setup Recomendado

1. **VM 1**: C2 Server (este sistema)
2. **VM 2**: Windows 10 (target)
3. **VM 3**: Ubuntu (target)
4. **VM 4**: Kali (attacker console)

**Red**: Isolated network o NAT

### Ejercicio 1: Reconocimiento
1. Conectar agentes
2. Enumerar sistema operativo
3. Listar usuarios
4. Identificar software

### Ejercicio 2: Network Discovery
1. Obtener configuración de red
2. Mapear tabla ARP
3. Identificar rutas
4. Encontrar recursos compartidos

### Ejercicio 3: Persistencia
1. Identificar mecanismos de startup
2. Listar tareas programadas
3. Enumerar servicios
4. (NO ejecutar sin permiso)

---

**¿Más preguntas?**

Consulta la documentación completa en:
- `/app/TUTORIAL_REDTEAM.md`
- `/app/README.md`
- `/app/QUICKSTART.md`
- `/app/REDTEAM_COMMANDS.md`

---

🛡️ **Stay Legal. Stay Ethical. Stay Secure.**
