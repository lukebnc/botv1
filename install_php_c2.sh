#!/bin/bash

# ============================================
# C2 Framework - Instalación Automática PHP
# ============================================

set -e

echo "========================================="
echo "  C2 Framework - PHP/MySQL Installation"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}[ERROR]${NC} This script must be run as root"
   exit 1
fi

# Step 1: Install Dependencies
echo -e "${YELLOW}[STEP 1]${NC} Installing dependencies..."
apt-get update -qq
apt-get install -y apache2 php php-mysql php-mbstring php-xml php-curl mysql-server > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Dependencies installed"

# Step 2: Import Database
echo -e "${YELLOW}[STEP 2]${NC} Creating database..."
mysql < /app/database.sql
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Database created successfully"
else
    echo -e "${RED}✗${NC} Database creation failed"
    exit 1
fi

# Step 3: Setup Backend
echo -e "${YELLOW}[STEP 3]${NC} Setting up PHP backend..."
mkdir -p /var/www/html/c2-api
cp -r /app/php-backend/* /var/www/html/c2-api/
chown -R www-data:www-data /var/www/html/c2-api
chmod -R 755 /var/www/html/c2-api
echo -e "${GREEN}✓${NC} Backend files copied"

# Step 4: Create .htaccess
echo -e "${YELLOW}[STEP 4]${NC} Creating .htaccess..."
cat > /var/www/html/c2-api/.htaccess << 'EOF'
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^api/(.*)$ /c2-api/index.php [QSA,L]
</IfModule>
EOF
echo -e "${GREEN}✓${NC} .htaccess created"

# Step 5: Configure Apache
echo -e "${YELLOW}[STEP 5]${NC} Configuring Apache..."
a2enmod rewrite > /dev/null 2>&1
cat > /etc/apache2/sites-available/c2-framework.conf << 'EOF'
<VirtualHost *:80>
    ServerName localhost
    DocumentRoot /var/www/html

    <Directory /var/www/html/c2-api>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/c2_error.log
    CustomLog ${APACHE_LOG_DIR}/c2_access.log combined
</VirtualHost>
EOF
a2ensite c2-framework > /dev/null 2>&1
systemctl restart apache2
echo -e "${GREEN}✓${NC} Apache configured"

# Step 6: Create directories
echo -e "${YELLOW}[STEP 6]${NC} Creating directories..."
mkdir -p /app/payloads
mkdir -p /app/screenshots
chown www-data:www-data /app/payloads
chown www-data:www-data /app/screenshots
chmod 755 /app/payloads
chmod 755 /app/screenshots
echo -e "${GREEN}✓${NC} Directories created"

# Step 7: Test Installation
echo -e "${YELLOW}[STEP 7]${NC} Testing installation..."
sleep 2
response=$(curl -s http://localhost/api/)
if [[ $response == *"C2 Framework API"* ]]; then
    echo -e "${GREEN}✓${NC} API is responding"
else
    echo -e "${RED}✗${NC} API test failed"
fi

# Step 8: Display Summary
echo ""
echo "========================================="
echo -e "  ${GREEN}Installation Complete!${NC}"
echo "========================================="
echo ""
echo "API Endpoint: http://localhost/api/"
echo "Dashboard: http://localhost:3000"
echo ""
echo "Default Credentials:"
echo "  Username: admin"
echo "  Password: c2admin123"
echo ""
echo "Database:"
echo "  Name: c2_framework"
echo "  User: c2_app"
echo "  Pass: C2SecurePassword123!"
echo ""
echo "Test API:"
echo "  curl http://localhost/api/"
echo ""
echo "Read full docs:"
echo "  cat /app/INSTALL_PHP.md"
echo ""
