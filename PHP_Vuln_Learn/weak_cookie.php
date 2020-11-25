<?php
//cookie明文 / 弱加密漏洞  demo

//include("mysqli.php");
# cookie明文 / 弱加密问题
if ($_SERVER['REQUEST_METHOD'] == "POST") {
	if (isset ($_COOKIE['id'])) {
		$_SESSION['id'] = $_COOKIE['id'] //admin
		result = mysqli_query("SELECT ticket from USERLIST WHERE USERNAME = '$_SESSION['id']'");

    while( $row = mysqli_fetch_assoc( $result ) ) {
        $ticket = $row["ticket"];
        echo "here is your ticket information: $ticket "; //明文cookie, 导致身份伪造
        }
	} else {
	setcookie("id", $cookie_value);
	}

}
?>