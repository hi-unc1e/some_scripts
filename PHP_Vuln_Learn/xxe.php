<?php
//xxe

$USERNAME = 'admin'; //账号
$PASSWORD = 'admin'; //密码
$result = null;

// 关键配置, 允许加载外部实体
libxml_disable_entity_loader(false);
$xmlfile = file_get_contents('php://input'); //输入流作为xml

try{
    # 解析xml结构
	$dom = new DOMDocument();
	$dom->loadXML($xmlfile, LIBXML_NOENT | LIBXML_DTDLOAD);
	$creds = simplexml_import_dom($dom);

	$username = $creds->username;
	$password = $creds->password;
    # 判断账号密码是否相等
	if($username == $USERNAME && $password == $PASSWORD){
		$result = sprintf("<result><code>%d</code><msg>%s</msg></result>",1,$username);
	}else{
		$result = sprintf("<result><code>%d</code><msg>%s</msg></result>",0,$username);
	}
	# 异常处理
}catch(Exception $e){
	$result = sprintf("<result><code>%d</code><msg>%s</msg></result>",3,$e->getMessage());
}
# 输出结果
header('Content-Type: text/html; charset=utf-8');
die($result);
?>