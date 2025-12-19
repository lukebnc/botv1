<?php
/**
 * Authentication Middleware
 */

require_once __DIR__ . '/../utils/JWT.php';

class Auth {
    public static function verifyToken() {
        $headers = getallheaders();
        
        if (!isset($headers['Authorization'])) {
            http_response_code(403);
            echo json_encode(['error' => 'No authorization header']);
            exit();
        }
        
        $authHeader = $headers['Authorization'];
        $token = str_replace('Bearer ', '', $authHeader);
        
        $payload = JWT::decode($token, SECRET_KEY);
        
        if (!$payload) {
            http_response_code(403);
            echo json_encode(['error' => 'Invalid or expired token']);
            exit();
        }
        
        return $payload;
    }
    
    public static function hashPassword($password) {
        return password_hash($password, PASSWORD_BCRYPT, ['cost' => 10]);
    }
    
    public static function verifyPassword($password, $hash) {
        return password_verify($password, $hash);
    }
}
?>