// Main.js - Code for the main (and probably only) page.

function renameIso(isoName, newName) {
  isoName = encodeURIComponent(isoName);
  newName = encodeURIComponent(newName);
  xhrGet("rename?type=dvd&iso=" + isoName + "&newname=" + newName, function() { 
    alert("successfully renamed!");
    location.reload();
  });
}

function searchMovieKeypress(e, isoName) {
  if (e.keyCode == 13) {
    searchMovie(isoName);
  }
}

function searchMovie(isoName) {

  var searchText = document.getElementById(isoName + "searchText");
  searchText.classList.remove("hidden");

  var rowIndex = 0;
  var getResultRow = function(title, year, id) {
    var row = document.createElement("div");
    row.id = "resultRow" + rowIndex++;
    row.className = "resultRow";
    row.addEventListener("click", function(evnt) {
      var thisElem = evnt.currentTarget;
      var allPrevElems = document.getElementsByClassName("lastClickedResultRow");
      for (var i = 0; i < allPrevElems.length; i++) {
        var prevElem = allPrevElems[i];
        if (prevElem) 
          prevElem.classList.remove("lastClickedResultRow");
      }
      thisElem.classList.toggle("lastClickedResultRow");
    }, false);

    var newName = title + " (" + year + ")";
    var titleLink = document.createElement("a");
    titleLink.href = "#";
    titleLink.addEventListener("click", function() { renameIso(isoName, newName); }, false);
    titleLink.className = "resultRowTitle";
    titleLink.innerHTML = title;
    row.appendChild(titleLink);

    var rightSpan = document.createElement("span");
    rightSpan.className = "resultRowRightLinks";
    row.appendChild(rightSpan);

    var yearP = document.createElement("p");
    yearP.className = "resultRowYear";
    yearP.innerHTML = "(" + year + ")";
    rightSpan.appendChild(yearP);

    var imdbLink = document.createElement("input");
    imdbLink.type = "button";
    imdbLink.addEventListener("click", function() { getImdb(id); }, false);
    imdbLink.value = "IMDB";
    rightSpan.appendChild(imdbLink);

    return row;
  };

  var searchString = document.getElementById(isoName + "searchString").value;
  searchString = encodeURIComponent(searchString);
  xhrGet("search?searchwords=" + searchString, function(resultObj) {
    var resultString;
    var resultsBox = document.getElementById(isoName + "resultsBox");
    resultsBox.innerHTML = ""; // remove existing results
    for (var i = 0; i < resultObj.results.length; i++) {
      var result = resultObj.results[i];
      resultsBox.appendChild(getResultRow(result.title, result.year, result.id));
    }
    searchText.classList.add("hidden");
  });
}

// Replace underscores with spaces and drop any extension after '.'
function fixTitleAndPaste(movieId, filename) {
  var fixedname = filename.substr(0, filename.lastIndexOf('.')).replace(/_/g, ' ');
  document.getElementById(movieId + "searchString").value = fixedname;
}

function getImdb(id) {
  xhrGet("imdbLink?mid=" + id, function(imdbIdObj) {
    if (imdbIdObj && imdbIdObj.hasOwnProperty("imdbid")) {
      window.open("http://imdb.com/title/" + imdbIdObj.imdbid, "_blank").focus();
    }
    else {
      alert("bad!");
    }
  });
}

// Show the popup and do some other stuff
function showPopupForIso(movieId, filename) {
  document.getElementById(movieId + 'popup').classList.remove('hidden');
  fixTitleAndPaste(movieId, filename);
  searchMovie(movieId);
}
