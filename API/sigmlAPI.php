<?php

// array to hold all the database configuration details
$config = array();

// Define if environment is production or development
// dev - Development Environment
// pro - Production Environment
$config['env'] = 'dev';
 
// setting $debug to true will echo out all the errors
$config['debug'] = TRUE;

if($config['env'] == 'pro') {
    // set the values for production environment
    $config['base_url'] = '';
    $config['db_host'] = '';
    $config['db_name'] = '';
    $config['db_user'] = '';
    $config['db_pass'] = '';
}

if ($config['env'] == 'dev') {
    // set the values for the development environment
    $config['base_url'] = 'http://localhost/text2sign/';
    $config['db_host'] = 'localhost';
    $config['db_name'] = 'text2sign';
    $config['db_user'] = 'root';
    $config['db_pass'] = 'root';
}

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

function dbconnect() {
	global $config;
	try {
		$db = new PDO('mysql:host='.$config['db_host'].';dbname='.$config['db_name'].';charset=utf8', $config['db_user'], $config['db_pass']);
		$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
		$db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
		return $db;
	} catch (Exception $e) {
		if($config['debug'])
			echo "ERROR : ".__file__." : ".$e->getMessage();
	}
}

/*
	Sigml API
	
	Checks if some sigml file exits or not and
	returns the filename if it exits
*/

$flag = False;

if(isset($_GET['action'])) {

	$action = $_GET['action'];
	$key = $_GET['q'];
	
	//  seacrh query should be only alpha numeric
	if(ctype_alnum($key))
    	$flag = True;
	else
		$flag = False;
	
	
	if($action == "search" && $flag == True) {
		try {
			$db = dbconnect();
			$query = "select * from sigmlFiles where name = ?";
			$stmt = $db->prepare($query);
			$stmt->execute(array($key));
			$result = $stmt->fetch(PDO::FETCH_ASSOC);
			if($result)
				$fileName = $result['fileName'];
			else
				$fileName = "FALSE";
			echo $fileName;
		} catch(Exception $e) {
			echo "ERROR : " . $e->getMessage();
		}
	}
	
}

?>
