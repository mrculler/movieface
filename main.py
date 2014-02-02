from flask import Flask, request, render_template
import os
import json
import tmdb
import re
from pprint import pprint

app = Flask(__name__)

@app.route("/")
def hello():
  bdIsos = sorted(os.listdir("movies/iso/hd"))
  dvdIsos = sorted(os.listdir("movies/iso/sd"))

  return render_template("main.html", isoListDvd=dvdIsos, isoListBd=bdIsos)

@app.route("/search")
def searchmovie():
  searchString = request.args.get("searchwords")
  print "searching for: " + searchString
  searchResults = tmdb.Movies(searchString)

  searchResultsSerializable = []
  for movie in searchResults.iter_results():
    print "  found: " + movie["title"]
    thisMovie = {}
    thisMovie["title"] = movie["title"]
    thisMovie["year"] = movie["release_date"][:4]
    thisMovie["id"] = movie["id"]
    """
    movieObj = tmdb.Movie(movie["id"])
    thisMovie["imdbId"] = movieObj.get_imdb_id()
    """
    searchResultsSerializable.append(thisMovie)
  return json.dumps({"results": searchResultsSerializable})

@app.route("/imdbLink")
def imdblink():
  movieId = request.args.get("mid")
  imdbId = tmdb.Movie(movieId).get_imdb_id()
  return json.dumps({"imdbid": imdbId})

@app.route("/rename")
def renameiso():
  isoType = request.args.get("type")
  isoFile = request.args.get("iso")
  newName = request.args.get("newname")
  
  # Get path
  if (isoType == "dvd"):
    pathPrefix = "movies/iso/sd/"
  elif (isoType == "bd"):
    pathPrefix = "movies/iso/bd/"
  else:
    return json.dumps({"error":"Invalid type {0}".format(isoType)})

  # Make sure the source file exists
  try:
    with open(pathPrefix + isoFile): pass
  except IOError:
    return json.dumps({"error":"File {0} does not exist!".format(pathPrefix + isoFile)})

  # Get rid of invalid characters in the name
  newName = re.sub("<3", "HEART", newName)
  newName = re.sub("[<>:\"/\\|\?\*]", "", newName)
  newName = re.sub("&", "and", newName)

  # Make sure the destination file does not already exist
  newNameComplete = pathPrefix + newName + ".iso"
  exists = True
  try:
    with open(newNameComplete): pass
  except IOError:
    exists = False

  if exists:
    return json.dumps({"error":"Destination filename {0} already exists!  Not renaming.".format(newNameComplete)})

  os.rename(pathPrefix + isoFile, newNameComplete)
  return json.dumps({})

if __name__ == "__main__":
  # Get API key from file, Configure TMDB API
  apiKeyFile = open('tmdb.api.key', 'r')
  tmdbApiKey = apiKeyFile.read().strip()
  tmdb.configure(tmdbApiKey)
  
  # We set iptables to redirect port 80 requests to port 5000, so the default port is ok here
  app.run(host="0.0.0.0", debug=True)
