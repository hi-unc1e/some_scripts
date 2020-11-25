<?php
//命令注入demo
//127.0.0.1; `sleep 1`
if( isset( $_POST[ 'admin' ]  ) ) {
	// Get input
	$target = $_REQUEST[ 'ip' ];
	// 黑名单
	$substitutions = array(
		'&&' => '',
		';'  => '',
		'||'  => '',
		'$'  => '',
	);

	// 替换黑名单字符串
	$target = str_replace( array_keys( $substitutions ), $substitutions, $target );

	// 操作系统
	if( stristr( php_uname( 's' ), 'Windows NT' ) ) {
		// Windows
		$cmd = shell_exec( 'ping  ' . $target );
	}
	else {
		// *nix
		$cmd = shell_exec( 'ping  -c 4 ' . $target );
	}

	// 输出结果
	$html .= "<pre>{$cmd}</pre>";
}

?>