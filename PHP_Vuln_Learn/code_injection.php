<?php
//php代码注入demo
error_reporting(0);
$pattern = $_GET['pat]';
$replacement = $_GET['rep'];
$subject = $_GET['sub'];

if ( isset($pattern) && isset($replacement) && isset($subject)){
    preg_replace($pattern, $replacement, $subject); //存在preg_replace /e 代码注入的风险
    //PAYLOAD => ?pat=/test/e&rep=phpinfo()&sub=test
} else {
    die();
}