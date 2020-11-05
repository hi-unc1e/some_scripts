
<?php
highlight_file(__FILE__);

$DIR = 'base';

if (!file_exists($DIR)) {
    @mkdir($DIR);
}

$src = file_get_contents('php://input');
if (preg_match("#^data:image/(\w+);base64,(.*)$#", $src, $matches)) {
    $appUrl = sprintf(
        "%s://%s%s",
        isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] != 'off' ? 'https' : 'http',
        $_SERVER['HTTP_HOST'],
        $_SERVER['REQUEST_URI']
    );
    $appUrl = str_replace("index.php", "", $appUrl);

    $base64 = $matches[2];
    $type = $matches[1];
    if ($type === 'jpeg') {
        $type = 'jpg';
    }

    $filename = md5($base64).".$type";
    $filePath = $DIR.DIRECTORY_SEPARATOR.$filename;
    
    if (file_exists($filePath)) {
        die('{"result" : "File Exists"}');
    } else {
        $data = base64_decode($base64);
        $res = "$appUrl"."base/"."$filename";
        file_put_contents($filePath, $data);
        die("{'result' : '$res'}}");
    }

} else {
    die("{'error' : {'code': 100, 'message': 'un recoginized source'}}");
}


