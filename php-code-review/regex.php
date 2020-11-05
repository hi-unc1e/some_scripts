<?php
error_reporting(0);
 function is_php($data){ //用正则判断是否为php代码
     return preg_match('/<\?.*[(`;?>].*/is', $data);//<? 
 }

$flag = is_php($_POST['p']);
if ($flag){ //
    echo "damn, really<br>"; //WAF notice
    var_dump($flag);
  	die();
}else{ //【恶意操作】
    echo "Good job!<br>";
    var_dump($flag);
    file_put_contents("./temp.php",$_POST['p']);// eval($_POST['p']);
}