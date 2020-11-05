<?php
error_reporting(0);
highlight_file(__FILE__);

if(preg_match('/SELECT.+FROM.+/is', $_POST['p'])) {
    die('SQL Injection');//WAF
}else{
    echo $_POST['p'];
}