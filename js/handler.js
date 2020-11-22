/*
        Load json file for sigml available for easy searching
    */
    $("#speech_loader").hide();
    $('#loader').hide();

    // $.getJSON("js/sigmlFiles.json", function(json){
    //     sigmlList = json;
    // });
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

    function getParsedText(speech) {
        // console.log("$$ 1");

        var HttpClient = function() {
            this.get = function(aUrl, aCallback) {
                var anHttpRequest = new XMLHttpRequest();
                anHttpRequest.onreadystatechange = function() {
                    if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                        aCallback(anHttpRequest.responseText);
                }

                anHttpRequest.open( "GET", aUrl, false );
                anHttpRequest.send( null );
            }
        };
        var final_response = "";
        var client = new HttpClient();
        client.get('http://localhost:5001/parser' + '?speech=' + speech, function(response) {
            console.log(response);
            final_response = JSON.parse(response);
        });
        // console.log("$$ 4");
        
        document.getElementById('isl').innerHTML = final_response['isl_text_string'];
        document.getElementById('speech_').innerHTML = speech; 
        return final_response['pre_process_string'];
    }
    activateTab("menu1-h", "menu1"); // activate first menu by default
    function startDictation() {
        $('#speech_recognizer').hide();
        $("#speech_loader").show();
        console.log('Speech recognition started...');

        if (window.hasOwnProperty('webkitSpeechRecognition')) {

            let recognition = new webkitSpeechRecognition();

            recognition.continuous = false;
            recognition.interimResults = false;

            recognition.lang = "en-US";
            recognition.start();

            recognition.onresult = function(e) {
                // document.getElementById('transcript').value = e.results[0][0].transcript;
                $('#speech_recognizer').show();
                $("#speech_loader").hide();
                $('#loader').show();

                console.log('Speech: ' + e.results[0][0].transcript);

                let speech = e.results[0][0].transcript;

                let parsedSpeech = getParsedText(speech);

                clickme(parsedSpeech);

                $('#loader').hide();

                recognition.stop();
                
                console.log('Speech recognition stopped...');

            };

            recognition.onerror = function(e) {
                recognition.stop();
            }

        }
    }

    var recognition = new webkitSpeechRecognition();
    recognition.continuous     = true;
    recognition.interimResults = true;

    recognition.onstart = function() {
        console.log("Recognition started");
    };
    recognition.onresult = function(event){
        var text = event.results[0][0].transcript;
        console.log(text);

        if (text === "stop avatar") {
            recognition.stop();
        }

        document.getElementById('dom-target').value = text;
        // clickme();

    };
    recognition.onerror = function(e) {
        console.log("Error");
    };

    // recognition.onend = function() {
    //     console.log("Speech recognition ended");
    // };

    function startDictation2() {
        recognition.lang = 'en-IN'; // 'en-US' works too, as do many others
        recognition.start();
    }

    function clickme(speech) {

        inputText = speech;
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
        console.log("sigmllength : "+sigmlList.length);
        for(x = 0; x < tokens.length; x++)
        {
            wordfoundflag = false;
            t = tokens[x];
            for(y = 0; y < sigmlList.length; y++) {
                if(sigmlList[y].name == t) {
                    // console.log(sigmlList[y].sid);
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
                    //q=q.toUpperCase();
                    for(k = 0; k < sigmlList.length; k++) {
                        if(sigmlList[k].name == q) {
                            wordArray[arrayCounter++] = new FinalText(q, sigmlList[k].fileName);
                            break;
                        }
                    }
                }
                max = 0,countit=0;

                for(k=0;k<sigmlList.length;k++)
                {
                    countit++;
                    if(sigmlList[k].sid>max)
                    { max = sigmlList[k].sid; }
                }
                console.log("maxi is : "+max);
                max = max + 1;
                if(t!="EOL"){
                    console.log("k is : "+k);
                    var obj = {"sid": max,"name": t,"fileName": t+".sigml"};

                    var newdata = JSON.stringify(sigmlList);
                    console.log(newdata);

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


    }
