<?php
require_once __DIR__ . '/../config/database.php';

class AuditLog {
    private $conn;
    private $table = 'audit_logs';
    
    public function __construct() {
        $database = new Database();
        $this->conn = $database->getConnection();
    }
    
    public function log($action, $user_id = null, $username = null, $node_id = null, $details = null) {
        $query = "INSERT INTO {$this->table} 
                  (action, user_id, username, node_id, details, ip_address, user_agent, timestamp) 
                  VALUES (:action, :user_id, :username, :node_id, :details, :ip_address, :user_agent, NOW())";
        $stmt = $this->conn->prepare($query);
        
        $ip_address = $_SERVER['REMOTE_ADDR'] ?? null;
        $user_agent = $_SERVER['HTTP_USER_AGENT'] ?? null;
        
        $stmt->bindParam(':action', $action);
        $stmt->bindParam(':user_id', $user_id);
        $stmt->bindParam(':username', $username);
        $stmt->bindParam(':node_id', $node_id);
        $stmt->bindParam(':details', $details);
        $stmt->bindParam(':ip_address', $ip_address);
        $stmt->bindParam(':user_agent', $user_agent);
        
        return $stmt->execute();
    }
    
    public function getRecent($limit = 100) {
        $query = "SELECT * FROM v_recent_activity LIMIT :limit";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':limit', $limit, PDO::PARAM_INT);
        $stmt->execute();
        return $stmt->fetchAll();
    }
}
?>