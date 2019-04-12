// list of puntutation marks for english language
englishpMarks = ["?", "!", "."];
hindipMarks = []; // include the hindi puntuation marks in UTF format

// array to store finally what is to played
wordArray = new Array();
function FinalText(word, fileName)
{
	this.word = word;
	this.fileName = fileName;
}
var arrayCounter = 0;

// global variable to put lock on the animation 
// to avoid race condition
var playerAvailableToPlay = true;

/*
	Check if this is sentence end for english language that is one of the
	puntuation marks then return true
*/
function isSentenceEndHindi(letter)
{
	// check if the letter is hindi | 
	// search for UTF-8 Hindi language to get more information
	if(letter.charCodeAt(0).toString(16) == "964")
		return true;
	return false;
}

/*
	Check if this is sentence end for english language that is one of the
	puntuation marks then return true
*/
function isSentenceEndEnglish(letter)
{
	// if letter is any of the english puntuation mark then
	// return true else return false
	for(x = 0; x < englishpMarks.length; x++) {
		if(letter == englishpMarks[x])
			return true;
	}
	return false;
}

/*
	Check if current letter is space or not
*/
function isSpace(letter)
{
	// check if the letter is a space
	if(letter.charCodeAt(0).toString(16) == "20")
		return true;
	return false;
}

/*
	Function to take paragraph input by the user and tokenize it.
	Returns the words in an array
*/
function tokenizeEnglish(inText)
{
	flag = false; // flag will be set true if the inText text will end with pMarks
	len = inText.length; 
	
	// the input should end with a punctuation mark
	for(x = 0; x < englishpMarks.length; x++) {
		// check if last character of the sentence is pMarks or not
		if(inText[len - 1] == englishpMarks[x]) {
			flag = true;
			break;
		}
	}
	
	// if no puntuation in the end then put a puntuation mark in the sentence
	if(flag == false)
		inputText = inText + ".";
	else
		inputText = inText;
	
	// convert the given paragraph into sentences 
	// result is an array holding each sentence own its own
	result = inputText.match( /[^\.!\?]+[\.!\?]+/g );
	console.log("tokenize into sentences : " + result);
	
	// convert each sentence into words and also add the pause 
	// identifier to make the animation pause after each word
	
	// loop over the result array and replace space and end of sentence 
	// and store it newString
	newString="";
	for(y = 0; y < result.length; y++) {
		line = result[y];
		for(x = 0; x < line.length; x++) {
			if(isSpace(line[x]))
				newString = newString + ",";
			else 
				newString = newString + line[x];
		}
		newString = newString + ",EOL,"; // EOL - end of line		
	}
	
	// create array of tokens
	console.log("Processed sting : " + newString);
	return newString;
}

function tokenizeHindi(inText)
{
	// implement the function to convert into the tokens here
	return intext;
}

/*
	Query API to check if sigml file exits or not
*/
function searchForSigml(key)
{
	$.ajax({ url: 'API/sigmlAPI.php?action=search&q=' + key, 
    	async: false,
    	success: function(data) {
    		console.log("Got data for " + key + " : " + data);
    		if(data=="FALSE")
    			return false;
    		else
    			return data;
     	}
    });
}


/*
	Hook for the button being clicked to run the animation
*/
$("#btnRun").click(function () {
	// read the input paragraph from the text box
	// trim it to remove any spaces from sides
	inputText = $("#inputText").val().trim();
	
	
	// read the language that has been set
	lang = "English"; // using english for default
	tokens = [];
	
	if(lang=="English") {
		
		// tokenize the english paragraph
		tokenString = tokenizeEnglish(inputText);
		tokens = tokenString.split(',');
		console.log("Got tokens"); 
		
	} else if(lang == "Hindi") {
		
		// tokenize the english paragraph
		tokenString = tokenizeHindi(inputText);
		tokens = tokenString.split(',');
		console.log("Got tokens"); 	
		
	}
		
	// remove empty values from tokens
	for(x = 0; x < tokens.length; x++) {
		t = tokens[x];
		
		if(t == "")
			tokens.splice(x, 1);
	}
	
	console.log(tokens);

	// process tokens based on language settings
	// use the script to generate the sigml files available and if
	// word file is available use word file less speak as letter based
	// list of sigmlfile is available in sigmlArray.js
	
		
	for(x = 0; x < tokens.length; x++) {
		// process each token
		t = tokens[x];	
		if(t == "EOL")
			continue;
		// convert token to lower case for seaching in the database
		// search for name and it will return filename if it will exists
		t = t.toLowerCase();
		t = t.replace('.',""); // remove the puntuation from the end
		tokens[x] = t;
	}
	
	console.log(tokens);
	
	// reset the wordArray and arrayCounter here
	wordArray = [];
	arrayCounter = 0;
	
	for(x = 0; x < tokens.length; x++) 
	{
		wordfoundflag = false;
		t = tokens[x];
		for(y = 0; y < sigmlList.length; y++) {
			if(sigmlList[y].name == t) {
				wordArray[arrayCounter++] = new FinalText(t, sigmlList[y].fileName);
				wordfoundflag = true;
				break;
			}
		}
		
		// if word not found then add chars - starts here
		if(wordfoundflag == false) {
			wordlen = t.length;
			for(p = 0; p < wordlen; p++) {
				q = t[p];
				for(k = 0; k < sigmlList.length; k++) {
					if(sigmlList[k].name == q) {
						wordArray[arrayCounter++] = new FinalText(q, sigmlList[k].fileName);
						break;
					}
				}				
			}
		}
		// if not word found part ends here
	}
	
	
	console.log(wordArray);
	console.log(wordArray.length);
	
	$("#debugger").html(JSON.stringify(wordArray));
	
	// wordArray object contains the word and corresponding files to be played
	// call the startPlayer on it in syn manner
	totalWords = wordArray.length;
	i = 0;
	
	var int = setInterval(function () {
		if(i == totalWords) {
			if(playerAvailableToPlay) {
				clearInterval(int);
				finalHint = $("#inputText").val();
				$("#textHint").html(finalHint);
			}			
		} else {
			if(playerAvailableToPlay) {
				playerAvailableToPlay = false;				
				startPlayer("SignFiles/" + wordArray[i].fileName);
				$("#textHint").html(wordArray[i].word);
				i++;
			}
		}
	}, 3000);
	
	
});
