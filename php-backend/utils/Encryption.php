<?php
/**
 * Encryption Utilities
 */

class Encryption {
    private static $method = 'AES-256-CBC';
    
    public static function encrypt($plaintext, $key) {
        $key = base64_decode($key);
        $iv = openssl_random_pseudo_bytes(openssl_cipher_iv_length(self::$method));
        $ciphertext = openssl_encrypt($plaintext, self::$method, $key, OPENSSL_RAW_DATA, $iv);
        
        return json_encode([
            'iv' => base64_encode($iv),
            'ciphertext' => base64_encode($ciphertext)
        ]);
    }
    
    public static function decrypt($encrypted, $key) {
        try {
            $data = json_decode($encrypted, true);
            $key = base64_decode($key);
            $iv = base64_decode($data['iv']);
            $ciphertext = base64_decode($data['ciphertext']);
            
            $plaintext = openssl_decrypt($ciphertext, self::$method, $key, OPENSSL_RAW_DATA, $iv);
            return $plaintext;
        } catch (Exception $e) {
            error_log("Decryption error: " . $e->getMessage());
            return false;
        }
    }
}
?>