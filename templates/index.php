<?php
$file = $_GET['file'] ?? 'index.html';
echo file_get_contents($file);
?>