<?php
//upload.php
$DIR = 'upload';
$src = file_get_contents('php://input');

if (preg_match("#^data:image/(\w+);base64,(.*)$#", $src, $matches)) {
    $appUrl = sprintf(
        "%s://%s%s",
        isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] != 'off' ? 'https' : 'http',
        $_SERVER['HTTP_HOST'],
        $_SERVER['REQUEST_URI']
    );
    $appUrl = str_replace("app.php", "", $appUrl);

    $base64 = $matches[2];
    $type = $matches[1];
    if ($type === 'jpeg') {
        $type = 'jpg';
    }

    $filename = md5($base64).".$type";
    $filePath = $DIR.DIRECTORY_SEPARATOR.$filename;

    if (file_exists($filePath)) {
        die('{"result" : "$appUrl".'upload/'."$filename"');
    } else {
        $data = base64_decode($base64);
        file_put_contents($filePath, $data);
        die('{"result" : "$appUrl".'upload/'."$filename"');
    }