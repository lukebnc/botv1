<?php
require_once __DIR__ . '/../config/database.php';

class Node {
    private $conn;
    private $table = 'nodes';
    
    public function __construct() {
        $database = new Database();
        $this->conn = $database->getConnection();
    }
    
    public function register($data) {
        $query = "CALL sp_register_node(:id, :hostname, :os, :ip, :token)";
        $stmt = $this->conn->prepare($query);
        
        $id = $this->generateUUID();
        $token = bin2hex(random_bytes(32));
        
        $stmt->bindParam(':id', $id);
        $stmt->bindParam(':hostname', $data['hostname']);
        $stmt->bindParam(':os', $data['os']);
        $stmt->bindParam(':ip', $data['ip']);
        $stmt->bindParam(':token', $token);
        
        if ($stmt->execute()) {
            return [
                'id' => $id,
                'hostname' => $data['hostname'],
                'os' => $data['os'],
                'ip' => $data['ip'],
                'token' => $token,
                'status' => 'online',
                'created_at' => date('c'),
                'last_seen' => date('c')
            ];
        }
        return false;
    }
    
    public function getAll() {
        $query = "SELECT * FROM {$this->table} ORDER BY last_seen DESC";
        $stmt = $this->conn->prepare($query);
        $stmt->execute();
        return $stmt->fetchAll();
    }
    
    public function getById($id) {
        $query = "SELECT * FROM {$this->table} WHERE id = :id";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':id', $id);
        $stmt->execute();
        return $stmt->fetch();
    }
    
    public function getByToken($token) {
        $query = "SELECT * FROM {$this->table} WHERE token = :token";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':token', $token);
        $stmt->execute();
        return $stmt->fetch();
    }
    
    public function updateStatus($id, $status) {
        $query = "UPDATE {$this->table} SET status = :status, last_seen = NOW() WHERE id = :id";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':id', $id);
        $stmt->bindParam(':status', $status);
        return $stmt->execute();
    }
    
    public function updateSysInfo($id, $data) {
        $query = "UPDATE {$this->table} SET 
                  cpu_usage = :cpu_usage,
                  memory_usage = :memory_usage,
                  disk_usage = :disk_usage,
                  processes = :processes,
                  last_seen = NOW()
                  WHERE id = :id";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':id', $id);
        $stmt->bindParam(':cpu_usage', $data['cpu_usage']);
        $stmt->bindParam(':memory_usage', $data['memory_usage']);
        $stmt->bindParam(':disk_usage', $data['disk_usage']);
        $stmt->bindParam(':processes', $data['processes']);
        return $stmt->execute();
    }
    
    public function delete($id) {
        $query = "DELETE FROM {$this->table} WHERE id = :id";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(':id', $id);
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