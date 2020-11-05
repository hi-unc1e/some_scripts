<?php
error_reporting(0);
highlight_file(__FILE__);

if(preg_match('/UNION.+?SELECT/is', $_POST['p'])) {
    die('SQL Injection');//WAF
}else{
    echo $_POST['p'];
}