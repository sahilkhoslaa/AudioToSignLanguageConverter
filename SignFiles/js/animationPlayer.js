    /* Code from TopIndex.html starts here */
    
	function startPlayer(objURL) {
		parent.appletframe.startPlayer(objURL);
	}
	
	function SetClass(event,clazz){
		var source;
		// Fix for old IE versions
		if (!event.target) { source = event.srcElement; } else { source = event.target; }
		if (source.tagName=="TR"||source.tagName=="TABLE")
			return;
		while(source.tagName!="TD") {
			// alert(source.tagName);
			source=source.parentNode;
		}
		source.className=clazz;
	}
	
	/* Code from TopIndex.html ends here */
	
	/* Code from applet.html starts here */

	function playText(stext) {
		CWASA.playSiGMLText(0, stext);
	}

	function setSiGMLURL(sigmlURL) {
		var loc = window.location.href;
		var locDir = loc.substring(0, loc.lastIndexOf('/'));
		// console.log("SiGML: "+sigmlURL);
		// console.log("Location Dir: "+locDir);
		sigmlURL = locDir + "/" + sigmlURL;
		// console.log("URL "+sigmlURL);
		document.getElementById("URLText").value = sigmlURL;
		return sigmlURL;
	}

	function startPlayer(sigmlURL) {
		sigmlURL = setSiGMLURL(sigmlURL);
		// Equivalent to click on Sign button
		CWASA.playSiGMLURL(0, sigmlURL);
	}

	/* Code from applet.html ends here */
