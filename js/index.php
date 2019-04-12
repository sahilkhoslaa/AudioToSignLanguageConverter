<!DOCTYPE html>
<html>
    <head>
    	<?php require_once("include.php"); ?>
        <title>ISL : Avatar Page</title>
        <meta http-equiv="Access-Control-Allow-Origin" content="*">
        <meta http-equiv="Access-Control-Allow-Methods" content="GET">
        <link rel="stylesheet" href="css/cwasa.css" />
        <script type="text/javascript" src="js/allcsa.js"></script>
        <script language="javascript">
			// Initial configuration
			var initCfg = {
				"avsbsl" : ["luna", "siggi", "anna", "marc", "francoise"],
				"avSettings" : { "avList": "avsbsl", "initAv": "marc" }
				};
				
			// global variable to store the sigmal list
			var sigmlList = null;

            // global variable to tell if avatar is ready or not
            var tuavatarLoaded = false;
		</script>
<script src="https://www.google.com/jsapi" type="text/javascript"></script>        
<script type="text/javascript">
  google.load("elements", "1", {
      packages: "transliteration"
    });
    function onLoad(){
      var options = {
        sourceLanguage: google.elements.transliteration.LanguageCode.ENGLISH,
        destinationLanguage: [google.elements.transliteration.LanguageCode.HINDI],
        shortcutKey: 'ctrl+g',
        transliterationEnabled: true
    };
    var control = new google.elements.transliteration.TransliterationControl(options);
    control.makeTransliteratable(['transliterateTextarea']);
    
  }
  google.setOnLoadCallback(onLoad);
  function myread(){
       var text=document.conversion.transliterateTextarea;
        var tcontent=text.value;
      window.alert(tcontent);
      return tcontent;
  }
  
</script>         
    </head>
    <body onload="CWASA.init(initCfg);" >
    <?php
    	include_once("nav.php");
    ?>      
    <div id="loading" class="container"><div class="row text-center"><span style="background-color:#ebf8a4; padding: 8px 20px;">Loading ... Please wait...</div></div></div>
        <!-- left side division starts here -->
		<div style="width:40%; padding:15px; float:left; margin-left:14%;">

<ul class="nav nav-tabs nav-justified" id="navi">
  <li role="presentation"><a href="#" id="menu1-h" onclick="activateTab('menu1-h', 'menu1');">English to Sign Language</a></li>
  <li role="presentation"><a href="#" id="menu2-h" onclick="activateTab('menu2-h', 'menu2');">Hindi to Sign Language</a></li>
  <!--<li role="presentation"><a href="#" id="menu3-h" onclick="activateTab('menu3-h', 'menu3');">Alphabets</a></li>
  <li role="presentation"><a href="#" id="menu4-h" onclick="activateTab('menu4-h', 'menu4');">Numbers</a></li>-->
</ul>

<div id="menu1">
<br>
<label for="inputText">Enter the text to convert to sign language:</label><br>
<textarea id="inputText" style="width:100%; height:80px;" autofocus></textarea><br><br>
<button type="button" id="btnRun" class="btn btn-primary">Parse and Generate Play Sequence</button>
<button type="button" id="btnClear" class="btn btn-default">Clear</button>
</div>

<div id="menu2">
<br>
<label for="inputText">Type text to convert to hindi:</label><br>
<textarea id="transliterateTextarea" name="transliterateTextarea" style="width:100%; height:80px;"></textarea>
</div>

<!--<div id="menu3">
<br>
Alphabets will be displayed here
</div>

<div id="menu4">
<br>
Number will be displayed here
</div>-->

<div id="debuggercontainer" style="margin-top:10px; border-top:3px solid black;">
	<br><strong>Debugger</strong></br>
	<div id="debugger"></div>
</div>
		</div> <!-- left side division ends here -->
<script language="javascript" src="js/animationPlayer.js"></script>		
		<?php 
			// This is the main player where the animation happens	
			include_once("animationPlayer.php"); 
		?>


<script type="text/javascript" src="js/player.js"></script>
<script type="text/javascript">
/*
	Load json file for sigml available for easy searching
*/
$.getJSON("js/sigmlFiles.json", function(json){
    sigmlList = json;
});

// code for clear button in input box for words
$("#btnClear").click(function() {
	$("#inputText").val("");
});

// code to check if avatar has been loaded or not and hide the loading sign
var loadingTout = setInterval(function() {
    if(tuavatarLoaded) {
        $("#loading").hide();
        clearInterval(loadingTout);
        console.log("Avatar loaded successfully !");
    }
}, 1000);


// code to animate tabs

alltabhead = ["menu1-h", "menu2-h", "menu3-h", "menu4-h"];
alltabbody = ["menu1", "menu2", "menu3", "menu4"];

function activateTab(tabheadid, tabbodyid)
{
    for(x = 0; x < alltabhead.length; x++)
        $("#"+alltabhead[x]).css("background-color", "white");
    $("#"+tabheadid).css("background-color", "#d5d5d5");
    for(x = 0; x < alltabbody.length; x++)
        $("#"+alltabbody[x]).hide();
    $("#"+tabbodyid).show();
}

activateTab("menu1-h", "menu1"); // activate first menu by default

</script>
<?php include_once("footer.php"); ?>
    </body>
</html>
