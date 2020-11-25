<?php
    //ssrf demo

    highlight_file(__FILE__);

  $url = $_GET['url'];
  if (preg_match("#^http:\/\/#", $url)){
  $curl = curl_init($url);

  /*进行curl配置*/
  curl_setopt($curl, CURLOPT_TIMEOUT, 10);  // 设置超时时间
  curl_setopt($curl, CURLOPT_HEADER, 0); // 不输出HTTP头
  curl_setopt($curl, CURLOPT_FOLLOWLOCATION, 1); //跟随跳转
    // curl_setopt($curl, CURLOPT_PROTOCOLS, CURLPROTO_HTTP|CURLPROTO_HTTPS|CURLPROTO_FILE); //限制cURL允许的协议
    $responseText = curl_exec($curl);

  /*打印curl结果*/
  //var_dump(curl_error($curl) );//如果执行curl过程中出现异常，可打开此开关，以便查看异常内容
  echo $responseText;

  /*关闭curl*/
  curl_close($curl);
  } else {
      die("Only allow http://");
  }
?>