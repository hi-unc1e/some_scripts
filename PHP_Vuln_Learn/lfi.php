<?php
// 本地文件包含LFI DEMO
$file = $_GET[ 'page' ];

// 过滤跳转符号
$file = str_replace( array( "../", "..\"" ), "", $file );

# 包含文件
$path = "/var/www/html/cms/system/" . $file
include($path);     //?page=..././..././..././..././..././..././/etc/passwd
?>