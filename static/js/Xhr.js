// Xhr.js - Simple XmlHttpRequest wrappers

// Send a basic XmlHttpRequest, expecting a JSON object as the reply.
// returnFunc is called with the reponse as its argument on success, otherwise errorFunc 
//  will be called (if it exists) with the response object.
// params is an object, where keys and values are serialized into the url request string
function xhrGet(baseurl, params, returnFunc, errorFunc) {
  var url = _serializeUrl(baseurl, params);

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

function _serializeUrl(url, params) {
  if (!params || isEmptyObject(params)) {
    return url;
  }
  var finalUrl = url + "?";
  var keys = Object.keys(params);
  for (var i = 0; i < keys.length; i++) {
    // We expect keys to be safe in urls.  Right, guys?  Right??
    var key = keys[i];
    var value = params[key];
    finalUrl += key + "=" + encodeURIComponent(value);
    if (i + 1 < keys.length) {
      finalUrl += "&";
    }
  }
  return finalUrl;
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
