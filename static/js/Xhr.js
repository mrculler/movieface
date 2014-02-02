// Xhr.js - Simple XmlHttpRequest wrappers

// Send a basic XmlHttpRequest, expecting a JSON object as the reply.
// returnFunc is called with the reponse as its argument on success, otherwise errorFunc 
//  will be called (if it exists) with the response object.
function xhrGet(url, returnFunc, errorFunc) {
  var request = new XMLHttpRequest();
  request.open("GET", url, true);
  request.onreadystatechange = function() {
    if ((request.readyState === 4) &&
        (request.status === 200)) {
      var responseObj = JSON.parse(request.responseText);
      if (responseObj.hasOwnProperty("error")) {
        if (errorFunc) {
          errorFunc(responseObj);
        }
        else {
          alert(responseObj.error);
        }
      }
      else {
        returnFunc(responseObj);
      }
    }
  }
  request.send();
}



/********************
 * Construction
 *******************/
// Set the XHR object for stupid browsers
if (typeof XMLHttpRequest == "undefined") {
  XMLHttpRequest = function () {
    try {
      return new ActiveXObject("Msxml2.XMLHTTP.6.0"); 
  }
    catch (e) {}
    try { 
      return new ActiveXObject("Msxml2.XMLHTTP.3.0"); 
  }
    catch (e) {}
    try {
      return new ActiveXObject("Microsoft.XMLHTTP");
  }
    catch (e) {}
    //Microsoft.XMLHTTP points to Msxml2.XMLHTTP and is redundant
    alert("This browser does not support XMLHttpRequest.");
  }
}
