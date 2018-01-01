<?php

$var = $_POST['inputText'];
#echo hello;
#echo $var;

$cmdd = './sc '.$var;
$cmdd = 'nano testt.txt';
echo $cmdd;
$cmddd = 'ls -la';
#echo $cmddd;
$output = shell_exec($cmdd);
echo "<pre>$output</pre>";



sleep(10);


$myfile = fopen("out.txt", "r") or die("Unable to open file!");
$ff="";
while(!feof($myfile)) {
  echo fgets($myfile) . "<br>";
}
fclose($myfile);



?>
