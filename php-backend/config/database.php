<?php
/**
 * Database Configuration
 * C2 Framework - PHP Backend
 */

class Database {
    private $host = 'localhost';
    private $db_name = 'c2_framework';
    private $username = 'c2_app';
    private $password = 'C2SecurePassword123!';
    private $charset = 'utf8mb4';
    public $conn;

    public function getConnection() {
        $this->conn = null;

        try {
            $dsn = "mysql:host={$this->host};dbname={$this->db_name};charset={$this->charset}";
            $options = [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES => false,
                PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci"
            ];
            
            $this->conn = new PDO($dsn, $this->username, $this->password, $options);
        } catch(PDOException $e) {
            error_log("Connection Error: " . $e->getMessage());
            die("Database connection failed");
        }

        return $this->conn;
    }
}
?>