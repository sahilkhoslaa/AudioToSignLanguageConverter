<!DOCTYPE html>
<html>
    <head>
    	<?php require_once("include.php"); ?>
        <title>ISL : Home Page</title>           
    </head>
    <body>
    <?php include_once("nav.php"); ?>
    <div class="container">
        <div class="row">
            <div class="col-md-12">
<!-- Put your code after this -->
		<h2>Working of Proposed System</h2>
		<p class="text-justify" style="line-height:1.8em;">For the proposed system input Hindi sentence will be processed by shallow parser to identify the higher syntactic and functional information of the sentence. It will perform the tasks of tokenization, morph analysis, part-of-speech tagging and chunking for the processing of an input sentence. The Hamburg sign language Notation System (HamNoSys) is a phonetic transcription system used to transcribe signing gestures. It is a syntactic representation of a sign to facilitate computer processing. The root words of input sentence will be mapped with HamNoSys notations with eSIGNEditor tool. eSIGNEditor will be used to pick signed sentences sign by sign from the lexicon and apply morphological changes to individual signs or strings of signs where necessary. After writing signs in HamNoSys, it will be converted into Signing Gesture Mark-up Language (SiGML). SiGML is a form of XML which defines a set of XML tags for each phonetic symbol in HamNoSys. Generated SiGML file will finally be processed by Signing Avatar like “JA SiGML URL APP”, which will play sign animation for the input text. The workflow of the proposed system has been given in below Figure.</p>
		<img class="center-block img-responsive" style="width:50%;" src="images/workflowOfProposedSystem.jpg">
		<h5 class="text-center">Fig:- Workflow of Proposed System </h5>

<!-- Put your code before this -->
            </div>
        </div>
    </div>
<?php include_once("footer.php"); ?>
	</body>
</html>	
