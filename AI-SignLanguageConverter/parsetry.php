<?php
$var = $_POST['inputText'];

$permanentcommand1 = "export STANFORDTOOLSDIR=$HOME";
$permanentcommand2 = "export CLASSPATH=$STANFORDTOOLSDIR/stanford-postagger-full-2015-04-20/stanford-postagger.jar:$STANFORDTOOLSDIR/stanford-ner-2015-04-20/stanford-ner.jar:$STANFORDTOOLSDIR/stanford-parser-full-2015-04-20/stanford-parser.jar:$STANFORDTOOLSDIR/stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models.jar";
$permanentcommand3 = "export STANFORD_MODELS=$STANFORDTOOLSDIR/stanford-postagger-full-2015-04-20/models:$STANFORDTOOLSDIR/stanford-ner-2015-04-20/classifiers";

$o1 = shell_exec($permanentcommand1);
$o2 = shell_exec($permanentcommand2);
$o3 = shell_exec($permanentcommand3);



#echo $var;
if($o3==""&&$o2==""&&$o1=="")
{
  $read = exec("python2.7 try.py ".$var);
  //$cmd = "python try.py ".$var;
  //$output = shell_exec($cmd);
  echo $read;
}
else echo "hey";

#sleep(10);


$myfile = fopen("out.txt", "r") or die("Unable to open file!");
$ff="";
while(!feof($myfile)) {
  echo fgets($myfile) . "<br>";
}
fclose($myfile);
?>