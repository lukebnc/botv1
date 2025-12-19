#!/bin/bash

# C2 Framework - Testing Script
# Educational purposes only

echo "========================================="
echo "   C2 Framework - Testing Suite"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Check Backend
echo -e "${YELLOW}[TEST 1]${NC} Checking Backend..."
response=$(curl -s http://localhost:8001/api/)
if [[ $response == *"C2 Framework API"* ]]; then
    echo -e "${GREEN}✓ Backend is running${NC}"
else
    echo -e "${RED}✗ Backend is NOT running${NC}"
    echo "  Start with: sudo supervisorctl restart backend"
    exit 1
fi

# Test 2: Check MongoDB
echo -e "${YELLOW}[TEST 2]${NC} Checking MongoDB..."
if pgrep -x "mongod" > /dev/null; then
    echo -e "${GREEN}✓ MongoDB is running${NC}"
else
    echo -e "${RED}✗ MongoDB is NOT running${NC}"
    echo "  Start with: sudo systemctl start mongod"
fi

# Test 3: Check Frontend
echo -e "${YELLOW}[TEST 3]${NC} Checking Frontend..."
if curl -s http://localhost:3000 > /dev/null; then
    echo -e "${GREEN}✓ Frontend is accessible${NC}"
else
    echo -e "${RED}✗ Frontend is NOT accessible${NC}"
    echo "  Start with: sudo supervisorctl restart frontend"
fi

# Test 4: Test Authentication
echo -e "${YELLOW}[TEST 4]${NC} Testing Authentication..."
auth_response=$(curl -s -X POST http://localhost:8001/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"c2admin123"}')

if [[ $auth_response == *"access_token"* ]]; then
    echo -e "${GREEN}✓ Authentication working${NC}"
    token=$(echo $auth_response | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    echo "  Token: ${token:0:20}..."
else
    echo -e "${RED}✗ Authentication failed${NC}"
fi

# Test 5: Check Node Registration
echo -e "${YELLOW}[TEST 5]${NC} Testing Node Registration..."
register_response=$(curl -s -X POST http://localhost:8001/api/nodes/register \
    -H "Content-Type: application/json" \
    -d '{"hostname":"test-node","os":"Linux","ip":"127.0.0.1"}')

if [[ $register_response == *"token"* ]]; then
    echo -e "${GREEN}✓ Node registration working${NC}"
    node_id=$(echo $register_response | grep -o '"id":"[^"]*' | cut -d'"' -f4)
    node_token=$(echo $register_response | grep -o '"token":"[^"]*' | cut -d'"' -f4)
    echo "  Node ID: $node_id"
    echo "  Node Token: ${node_token:0:20}..."
else
    echo -e "${RED}✗ Node registration failed${NC}"
fi

# Test 6: Get Nodes List
if [ ! -z "$token" ]; then
    echo -e "${YELLOW}[TEST 6]${NC} Getting Nodes List..."
    nodes_response=$(curl -s http://localhost:8001/api/nodes \
        -H "Authorization: Bearer $token")
    
    if [[ $nodes_response == *"["* ]]; then
        echo -e "${GREEN}✓ Nodes endpoint working${NC}"
        node_count=$(echo $nodes_response | grep -o '"id"' | wc -l)
        echo "  Total nodes: $node_count"
    else
        echo -e "${RED}✗ Nodes endpoint failed${NC}"
    fi
fi

# Test 7: Get Statistics
if [ ! -z "$token" ]; then
    echo -e "${YELLOW}[TEST 7]${NC} Getting Statistics..."
    stats_response=$(curl -s http://localhost:8001/api/stats \
        -H "Authorization: Bearer $token")
    
    if [[ $stats_response == *"total_nodes"* ]]; then
        echo -e "${GREEN}✓ Statistics endpoint working${NC}"
        echo "  Stats: $stats_response"
    else
        echo -e "${RED}✗ Statistics endpoint failed${NC}"
    fi
fi

echo ""
echo "========================================="
echo "   Testing Complete!"
echo "========================================="
echo ""
echo "Next Steps:"
echo "1. Access Dashboard: http://localhost:3000"
echo "2. Login with: admin / c2admin123"
echo "3. Run agent: python3 /app/agent.py"
echo ""
echo "For full tutorial, see: /app/TUTORIAL_REDTEAM.md"
