<?php
require_once __DIR__ . '/../config/database.php';

class Command {
    private $conn;
    private $table = 'commands';
    
    public function __construct() {
        $database = new Database();
        $this->conn = $database->getConnection();
    }
    
    public function create($data) {
        $query = "INSERT INTO {$this->table} (id, node_id, command, status, timestamp) 
                  VALUES (:id, :node_id, :command, :status, NOW())";
        $stmt = $this->conn->prepare($query);
        
        $id = $this->generateUUID();
        $status = 'pending';
        
        $stmt->bindParam(':id', $id);
        $stmt->bindParam(':node_id', $data['node_id']);
        $stmt->bindParam(':command', $data['command']);
        $stmt->bindParam(':status', $status);
        
        if ($stmt->execute()) {
            return [
                'id' => $id,
                'node_id' => $data['node_id'],
                'command' => $data['command'],
                'status' => $status,
                'timestamp' => date('c')
            ];
        }
        return false;
    }
    
    public function getAll($node_id = null) {
        if ($node_id) {
            $query = "SELECT * FROM {$this->table} WHERE node_id = :node_id ORDER BY timestamp DESC";
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':node_id', $node_id);
        } else {
            $query = "SELECT * FROM {$this->table} ORDER BY timestamp DESC LIMIT 1000";
            $stmt = $this->conn->prepare($query);
        }
        $stmt->execute();
        return $stmt->fetchAll();
    }
    
    public function updateResult($id, $result, $status) {
        $query = "UPDATE {$this->table} SET 
                  result = :result, 
                  status = :status,
                  executed_at = NOW()
                  WHERE id = :id";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':id', $id);
        $stmt->bindParam(':result', $result);
        $stmt->bindParam(':status', $status);
        return $stmt->execute();
    }
    
    private function generateUUID() {
        return sprintf('%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
            mt_rand(0, 0xffff), mt_rand(0, 0xffff),
            mt_rand(0, 0xffff),
            mt_rand(0, 0x0fff) | 0x4000,
            mt_rand(0, 0x3fff) | 0x8000,
            mt_rand(0, 0xffff), mt_rand(0, 0xffff), mt_rand(0, 0xffff)
        );
    }
}
?>