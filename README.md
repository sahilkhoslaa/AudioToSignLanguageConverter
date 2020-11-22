# Audio to Sign Language Translator
A web based application which accepts Audio/ Voice as input and converts it to corresponding Sign Language for Deaf people.
The interface works in two phases, 
* First, recognizes speech and converts it to text using JavaScript Web Speech API 
* Secondly, uses Machine based translation to translate English into ISL based grammar. Semi-structured parse tree of English text is modified to represent parse tree of ISL based on bi-linguistic rules.

![Scrrenshot](https://github.com/sahilkhoslaa/AudioToSignLanguageConverter/blob/master/images/Screenshot.png)
## Installation Guide

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
* ```Python >= 2.7```
* ```Browser supports Web Speech API```


### Installing
* Git clone repository
* Download all required packages for running python script server.py
* Download the zip : [Stanford Parser](https://nlp.stanford.edu/software/stanford-parser-full-2018-10-17.zip)
* Extract the zip file into a Directory. Don't rename it and place the directory inside 'AudioToSignLanguageConverter' directory where all files like server.py etc are present.
* Host the index.html in localhost or your own server to see avatar in action as it requires calls over http to download meta data else you may encouter some issue which can be inspected through console log.
* Make sure you are using Google Chrome.

### Running the code
* Run flask application server.py in localhost or server. Running server.py first time takes too long as it downloads 
Stanford-Parser over HTTP. Make sure you are connected to internet.
* Run index.html in browsers

Say something!! (The code will parse your speech and avatar will enact your phrase.)
 
## Authors
See the list of [contributors](https://github.com/sahilkhoslaa/AudioToSignLanguageConverter/contributors) who participated in this project.


