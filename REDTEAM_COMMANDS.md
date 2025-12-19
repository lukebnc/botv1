# 🎯 Red Team Commands Reference

## ⚠️ USAR SOLO EN ENTORNOS AUTORIZADOS

Esta es una referencia de comandos útiles para ejercicios de Red Team en sistemas con autorización explícita.

---

## 📋 Índice por Fase

1. [Reconocimiento](#reconocimiento)
2. [Enumeración](#enumeración)
3. [Información de Red](#información-de-red)
4. [Procesos y Servicios](#procesos-y-servicios)
5. [Usuarios y Grupos](#usuarios-y-grupos)
6. [Sistema de Archivos](#sistema-de-archivos)
7. [Seguridad y Defensas](#seguridad-y-defensas)
8. [Persistencia](#persistencia)

---

## 🔍 Reconocimiento

### Windows
```cmd
# Información básica del sistema
systeminfo
hostname
ver
wmic computersystem get domain

# Información de hardware
wmic cpu get name
wmic memorychip get capacity
wmic diskdrive get size,model

# Variables de entorno
set
echo %USERNAME%
echo %COMPUTERNAME%
echo %USERDOMAIN%

# Arquitectura
wmic os get osarchitecture
```

### Linux/Mac
```bash
# Información del sistema
uname -a
hostnamectl
cat /etc/os-release
cat /etc/*release*

# Hardware
lscpu
free -h
df -h
lsblk

# Variables de entorno
env
printenv
echo $USER
echo $HOME

# Arquitectura
arch
dpkg --print-architecture
```

---

## 📊 Enumeración

### Windows
```cmd
# Software instalado
wmic product get name,version
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall

# Actualizaciones instaladas
wmic qfe list

# Programas en ejecución al inicio
wmic startup get caption,command

# Tareas programadas
schtasks /query /fo LIST
schtasks /query /fo LIST /v

# Información de antivirus
wmic /namespace:\\root\securitycenter2 path antivirusproduct GET displayName,productState

# Firewall status
netsh advfirewall show allprofiles
```

### Linux
```bash
# Software instalado
dpkg -l                    # Debian/Ubuntu
rpm -qa                    # RedHat/CentOS
pacman -Q                  # Arch

# Servicios
systemctl list-units --type=service
service --status-all

# Cron jobs
crontab -l
cat /etc/crontab
ls -la /etc/cron.*

# Firewall
iptables -L -n
ufw status

# SELinux/AppArmor
sestatus
aa-status
```

---

## 🌐 Información de Red

### Windows
```cmd
# Configuración de red
ipconfig /all
netsh interface show interface
netsh interface ip show config

# Tabla ARP
arp -a

# Rutas
route print
netsh interface ip show route

# DNS cache
ipconfig /displaydns

# Conexiones activas
netstat -ano
netstat -ano | findstr LISTENING
netstat -ano | findstr ESTABLISHED

# Recursos compartidos
net share
net use

# WIFI profiles
netsh wlan show profiles
netsh wlan show profile name="WIFI_NAME" key=clear
```

### Linux/Mac
```bash
# Configuración de red
ifconfig -a
ip addr show
ip link show

# Tabla ARP
arp -a
ip neigh

# Rutas
route -n
ip route show

# DNS
cat /etc/resolv.conf

# Conexiones activas
netstat -tuln
ss -tuln
lsof -i

# Recursos compartidos
showmount -e localhost
smbclient -L localhost

# WIFI (requiere permisos)
iwconfig
nmcli device wifi list
```

---

## 🖥️ Procesos y Servicios

### Windows
```cmd
# Listar procesos
tasklist
tasklist /v
tasklist /svc

# Procesos con conexiones de red
netstat -ano

# Información detallada de proceso
wmic process where name="process.exe" get commandline,processid

# Servicios
net start
sc query
wmic service list brief

# Drivers
driverquery
```

### Linux
```bash
# Procesos
ps aux
ps -ef
top -n 1
htop

# Árbol de procesos
pstree

# Procesos con conexiones
netstat -tulpn
ss -tulpn
lsof -i

# Servicios
systemctl list-units --type=service --state=running
service --status-all | grep +

# Módulos del kernel
lsmod
```

---

## 👥 Usuarios y Grupos

### Windows
```cmd
# Usuario actual
whoami
whoami /all
whoami /priv
whoami /groups

# Todos los usuarios
net user
net localgroup

# Administradores
net localgroup administrators
net localgroup "Administradores"

# Usuarios conectados
query user
qwinsta

# Sesiones
net session
```

### Linux
```bash
# Usuario actual
whoami
id
groups

# Todos los usuarios
cat /etc/passwd
cat /etc/shadow    # requiere root
getent passwd

# Usuarios con shell
cat /etc/passwd | grep -v nologin

# Grupos
cat /etc/group
getent group

# Usuarios conectados
w
who
last
lastlog

# Sudoers
sudo -l
cat /etc/sudoers
```

---

## 📁 Sistema de Archivos

### Windows
```cmd
# Directorios importantes
dir C:\Users
dir C:\Windows\System32
dir C:\Program Files
dir C:\ProgramData

# Archivos recientes
dir C:\Users\%USERNAME%\Recent

# Buscar archivos
dir /s /b C:\*.txt
dir /s /b C:\*.config
dir /s /b C:\*password*

# Permisos
icacls "C:\path\file"

# Archivos ocultos
dir /a:h

# Drives
wmic logicaldisk get name,description,filesystem
```

### Linux
```bash
# Directorios importantes
ls -la /home
ls -la /etc
ls -la /var/www
ls -la /opt

# Archivos recientes
find /home -type f -mtime -7

# Buscar archivos
find / -name "*.conf" 2>/dev/null
find / -name "*password*" 2>/dev/null
find / -name "*.key" 2>/dev/null

# Permisos
ls -la
find / -perm -4000 2>/dev/null  # SUID
find / -perm -2000 2>/dev/null  # SGID

# Archivos con capabilities
getcap -r / 2>/dev/null

# Discos montados
mount
df -h
cat /etc/fstab
```

---

## 🔒 Seguridad y Defensas

### Windows
```cmd
# Política de seguridad
secedit /export /cfg security_policy.inf

# Logs de eventos
wevtutil el                           # Listar logs
wevtutil qe Security /c:10 /rd:true  # Leer Security log

# UAC status
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA

# Defender status
Get-MpComputerStatus    # PowerShell
sc query WinDefend

# AMSI bypass (educational)
# Not recommended to share specific bypasses
```

### Linux
```bash
# Logs del sistema
tail -f /var/log/syslog
tail -f /var/log/auth.log
journalctl -f

# Intentos de login fallidos
cat /var/log/auth.log | grep "Failed password"

# SELinux
getenforce
sestatus

# AppArmor
aa-status

# Auditd
auditctl -l
ausearch -m user_login

# Fail2ban
fail2ban-client status
```

---

## 🔄 Persistencia

### ⚠️ SOLO EN SISTEMAS AUTORIZADOS

### Windows
```cmd
# Tareas programadas (ver, no crear)
schtasks /query /fo LIST /v

# Inicio automático (ver)
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run

# Servicios (ver)
sc query
wmic service list brief
```

### Linux
```bash
# Cron jobs (ver)
crontab -l
cat /etc/crontab
ls -la /etc/cron.*

# Systemd services (ver)
systemctl list-units --type=service

# RC scripts (ver)
ls -la /etc/rc*.d/

# Bash profiles (ver)
cat ~/.bashrc
cat ~/.bash_profile
cat /etc/profile
```

---

## 🎯 Comandos por Objetivo

### Objetivo: Reconocimiento Inicial

**Windows:**
```cmd
systeminfo && hostname && whoami && ipconfig /all
```

**Linux:**
```bash
uname -a && hostname && whoami && ifconfig -a
```

### Objetivo: Información de Red Completa

**Windows:**
```cmd
ipconfig /all && arp -a && route print && netstat -ano
```

**Linux:**
```bash
ip addr && ip route && arp -a && netstat -tuln
```

### Objetivo: Enumeración de Usuarios

**Windows:**
```cmd
whoami /all && net user && net localgroup administrators
```

**Linux:**
```bash
id && cat /etc/passwd && sudo -l
```

### Objetivo: Procesos y Servicios

**Windows:**
```cmd
tasklist /v && net start && sc query
```

**Linux:**
```bash
ps aux && systemctl list-units --type=service --state=running
```

---

## 🔥 One-Liners Útiles

### Windows
```cmd
# Todo en uno - Reconocimiento básico
systeminfo & hostname & whoami & ipconfig /all & net user & tasklist & netstat -ano

# Buscar archivos sensibles
dir /s /b C:\*password*.txt C:\*config*.xml C:\*.key

# Información de dominio
echo %USERDOMAIN% & echo %LOGONSERVER% & net config workstation
```

### Linux
```bash
# Todo en uno - Reconocimiento básico
uname -a; hostname; whoami; id; ifconfig; netstat -tuln; ps aux

# Buscar archivos sensibles
find / -name "*password*" -o -name "*.key" -o -name "*secret*" 2>/dev/null

# Enumerar todo
(whoami && id && hostname && cat /etc/os-release && ip addr && ps aux) 2>/dev/null
```

---

## 📝 Notas de Uso

### Para cada comando:
1. **Verificar permisos**: Algunos comandos requieren privilegios elevados
2. **Revisar logs**: Tu actividad puede quedar registrada
3. **Timing**: Algunos comandos generan ruido en el sistema
4. **Ofuscación**: En ejercicios reales, considera técnicas de evasión

### Buenas Prácticas:
- ✅ Documentar cada acción
- ✅ Mantener logs de tus comandos
- ✅ Usar comandos nativos del sistema
- ✅ Conocer cómo revertir cambios

### Evitar:
- ❌ Comandos que dañen el sistema
- ❌ Borrar logs sin autorización
- ❌ Modificar archivos críticos
- ❌ Crear backdoors permanentes

---

## 🎓 Framework MITRE ATT&CK

Estos comandos mapean a las siguientes tácticas de MITRE ATT&CK:

- **Reconnaissance**: systeminfo, uname, ifconfig
- **Discovery**: net user, ps aux, netstat
- **Collection**: dir, find, cat
- **Credential Access**: whoami /priv, sudo -l
- **Persistence**: schtasks, crontab

Para más información: https://attack.mitre.org/

---

## 🔗 Recursos Adicionales

### Cheat Sheets
- [Windows Commands](https://ss64.com/nt/)
- [Linux Commands](https://ss64.com/bash/)
- [SANS Posters](https://www.sans.org/posters/)

### Herramientas
- PowerShell for Red Team
- Linux Privilege Escalation
- Windows Privilege Escalation

### Frameworks
- MITRE ATT&CK
- Lockheed Martin Cyber Kill Chain
- Diamond Model

---

## ⚖️ Legal y Ético

**Recuerda:**
- Estos comandos son para EDUCACIÓN y uso AUTORIZADO
- Siempre ten permiso POR ESCRITO
- Respeta las leyes locales e internacionales
- Mantén la confidencialidad de la información
- Reporta hallazgos responsablemente

---

## 📞 En el Dashboard C2

Para usar estos comandos:

1. **Selecciona un nodo** en la pestaña "Nodes"
2. **Copia el comando** de esta referencia
3. **Pégalo** en el campo de comando
4. **Presiona Execute**
5. **Revisa resultados** en Command History

---

**Desarrollado para Red Team Profesional**

🛡️ **Stay Legal. Stay Ethical. Stay Secure.**
