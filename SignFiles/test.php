<!DOCTYPE html>
<html>
    <head>
    	<?php require_once("include.php"); ?>
        <title>Test</title>
        <script type="text/javascript" src="js/jquery.min.js"></script>
    </head>
    <body>
    <div class="container">
    <div class="row">
    	<div class="col-md-6">
			<h1>Parsing test</h1>
			<hr>
			<label for="lang">Select langauge:</label><br>
			<input type="radio" value="Hindi" id="lang" name="lang" checked> Hindi<br>
			<input type="radio" value="English" id="lang" name="lang"> English <br><br>
			<label for="line">Given sentence input below:</label>
			<textarea name="line" id="line" style="width:100%; height:70px;" autofocus class="form-control"></textarea><br>
			<button type="button" id="process" class="btn btn-primary">Process Input</button>
		</div>
		<div class="col-md-6">
			<h1>Result</h2>
			<hr>
			<textarea id="result" style="width:100%; height:300px; overflow-y:scroll;" readonly></textarea>
			
			</div>
		</div>
	</div> <!-- Row ends here -->
	</div> <!-- Container ends here -->
	<script type="text/javascript" src="js/parser.js"></script>
	</body>
</html>	
