<?php
/**
 * Application Configuration
 */

define('SECRET_KEY', 'your-secret-jwt-key-change-in-production');
define('AES_KEY', 'ba4gd0qnveoxHglI4OL8n0jRAteGLexoWN2FbOH2zsU=');
define('JWT_EXPIRATION', 3600); // 1 hour
define('ALLOWED_ORIGINS', '*');
define('WEBSOCKET_PORT', 8080);
define('MAX_UPLOAD_SIZE', 104857600); // 100MB
define('PAYLOADS_DIR', '/app/payloads');
define('SCREENSHOTS_DIR', '/app/screenshots');

// Timezone
date_default_timezone_set('UTC');

// Error reporting (disable in production)
error_reporting(E_ALL);
ini_set('display_errors', 1);

// CORS Headers
header('Access-Control-Allow-Origin: ' . ALLOWED_ORIGINS);
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');
header('Access-Control-Allow-Credentials: true');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}
?>