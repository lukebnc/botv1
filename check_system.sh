#!/bin/bash

# Script de Verificación Visual del Sistema C2

clear

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════╗"
echo "║   C2 FRAMEWORK - ESTADO DEL SISTEMA     ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Function to check service
check_service() {
    local service=$1
    local status=$(sudo supervisorctl status $service 2>/dev/null | awk '{print $2}')
    
    if [ "$status" == "RUNNING" ]; then
        echo -e "${GREEN}✓${NC} $service: ${GREEN}CORRIENDO${NC}"
        return 0
    else
        echo -e "${RED}✗${NC} $service: ${RED}DETENIDO${NC}"
        return 1
    fi
}

# Check Services
echo -e "${YELLOW}[1] SERVICIOS${NC}"
echo "─────────────────────────────────────────"
check_service "backend"
check_service "frontend"
check_service "mongodb"
echo ""

# Check API
echo -e "${YELLOW}[2] API BACKEND${NC}"
echo "─────────────────────────────────────────"
response=$(curl -s http://localhost:8001/api/ 2>/dev/null)
if [[ $response == *"C2 Framework"* ]]; then
    echo -e "${GREEN}✓${NC} API respondiendo correctamente"
    echo -e "  ${CYAN}URL:${NC} http://localhost:8001/api/"
else
    echo -e "${RED}✗${NC} API no responde"
fi
echo ""

# Check Frontend
echo -e "${YELLOW}[3] PANEL WEB${NC}"
echo "─────────────────────────────────────────"
frontend_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null)
if [ "$frontend_status" == "200" ]; then
    echo -e "${GREEN}✓${NC} Panel web accesible"
    echo -e "  ${CYAN}URL:${NC} http://localhost:3000"
else
    echo -e "${RED}✗${NC} Panel web no accesible"
fi
echo ""

# Check Database
echo -e "${YELLOW}[4] BASE DE DATOS${NC}"
echo "─────────────────────────────────────────"
mongo_status=$(pgrep mongod >/dev/null && echo "running" || echo "stopped")
if [ "$mongo_status" == "running" ]; then
    echo -e "${GREEN}✓${NC} MongoDB corriendo"
    # Try to count documents
    node_count=$(mongo c2_framework --quiet --eval "db.nodes.count()" 2>/dev/null || echo "0")
    echo -e "  ${CYAN}Nodos registrados:${NC} $node_count"
else
    echo -e "${RED}✗${NC} MongoDB detenido"
fi
echo ""

# Check Files
echo -e "${YELLOW}[5] ARCHIVOS IMPORTANTES${NC}"
echo "─────────────────────────────────────────"
files=(
    "/app/backend/server.py:Backend Python"
    "/app/frontend/src/App.js:Frontend React"
    "/app/agent_advanced.py:Agente Avanzado"
    "/app/database.sql:Schema MySQL"
    "/app/php-backend/index.php:Backend PHP"
)

for file_info in "${files[@]}"; do
    IFS=':' read -r file desc <<< "$file_info"
    if [ -f "$file" ]; then
        size=$(du -h "$file" | cut -f1)
        echo -e "${GREEN}✓${NC} $desc ${CYAN}($size)${NC}"
    else
        echo -e "${RED}✗${NC} $desc ${RED}(no encontrado)${NC}"
    fi
done
echo ""

# Check Payloads
echo -e "${YELLOW}[6] PAYLOADS GENERADOS${NC}"
echo "─────────────────────────────────────────"
if [ -d "/app/payloads" ]; then
    payload_count=$(ls -1 /app/payloads 2>/dev/null | wc -l)
    if [ $payload_count -gt 0 ]; then
        echo -e "${GREEN}✓${NC} $payload_count payload(s) generado(s)"
        ls -lh /app/payloads | tail -n +2 | while read -r line; do
            echo -e "  ${CYAN}→${NC} $(echo $line | awk '{print $9, "("$5")"}')"
        done
    else
        echo -e "${YELLOW}⚠${NC} No hay payloads generados"
    fi
else
    echo -e "${YELLOW}⚠${NC} Directorio de payloads no existe"
fi
echo ""

# Check Network
echo -e "${YELLOW}[7] CONFIGURACIÓN DE RED${NC}"
echo "─────────────────────────────────────────"
ip_address=$(hostname -I | awk '{print $1}')
echo -e "${GREEN}✓${NC} IP del servidor: ${CYAN}$ip_address${NC}"
echo ""
echo -e "  ${BLUE}Acceder desde otra PC:${NC}"
echo -e "  http://$ip_address:3000"
echo ""

# Summary
echo "═══════════════════════════════════════════"
echo -e "${CYAN}RESUMEN${NC}"
echo "═══════════════════════════════════════════"
echo ""
echo -e "${GREEN}✓ ACCESO RÁPIDO:${NC}"
echo -e "  Panel Web:    ${CYAN}http://localhost:3000${NC}"
echo -e "  Desde otra PC: ${CYAN}http://$ip_address:3000${NC}"
echo ""
echo -e "${GREEN}✓ CREDENCIALES:${NC}"
echo -e "  Usuario:  ${CYAN}admin${NC}"
echo -e "  Password: ${CYAN}c2admin123${NC}"
echo ""
echo -e "${GREEN}✓ EJECUTAR AGENTE:${NC}"
echo -e "  ${CYAN}python3 /app/agent_advanced.py${NC}"
echo ""
echo -e "${GREEN}✓ COMANDOS ÚTILES:${NC}"
echo -e "  Ver logs:     ${CYAN}tail -f /var/log/supervisor/backend.out.log${NC}"
echo -e "  Reiniciar:    ${CYAN}sudo supervisorctl restart all${NC}"
echo -e "  Ver guía:     ${CYAN}cat /app/GUIA_SIMPLE.md${NC}"
echo ""
