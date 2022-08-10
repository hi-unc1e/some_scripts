<?php
//用于SSRF探测
$url = $_GET['url'];
header("Location: $url");

?>
