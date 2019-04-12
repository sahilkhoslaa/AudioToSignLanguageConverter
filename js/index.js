(function (window) {
    var TextToSpeech = {
        _key: "addf7ce48a11e371d6fa2a7b6075b9937ab=a6e2f7e1be80d86db2f56bd67953b0bb"
      , _lang: "en"
      , _voiceId: "en_gb_amy"

        /**
         * talk
         * Convert the provided text into speech.
         *
         * @name talk
         * @function
         * @param {Object} options An object containing:
         *
         *   - text: a string that must be converted in speech
         *   - notNow (default: false): don't play it now
         *
         * @param {Boolean} notNow Autoplay or not.
         * @return {Audio} The `Audio` instance.
         */
       , talk: function (options, notNow) {

            if (!options) {
                throw new Error("Please provide options.");
            }

            // handle string values
            if (typeof options === "string") {
                options = {
                    text: options
                };
            }

            // encode text
            options.text = btoa (options.text);

            // convert to boolean
            notNow = Boolean(notNow);

            // set the tts url
            var voiceId = btoa(options.voiceId || TextToSpeech._voiceId)
              , language = options.lang || TextToSpeech._lang
              , key = options.key || TextToSpeech._key
              , ttsUrl = "http://www.ivona.com/voicetest.php?rtr=1&t2r=" + options.text + "&v2r=" + voiceId + "&lang=" + language + "&" + key
              , thisSpeech = new Audio(ttsUrl)
              ;

            // if not now is false, play it
            if (!notNow) {
                thisSpeech.play();
            }

            // return audio object to the user
            return thisSpeech;
        }
    };

    window.TextToSpeech = TextToSpeech;
})(window);
