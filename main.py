from flask import Flask, request, render_template
import os
import re
import json
import urllib
import easytmdb as tmdb
from pprint import pprint

from face_types import Collection, Movie
from facedb import FaceDB
import facefs

app = Flask(__name__)

@app.route("/")
def hello():
  # Update big_dict
  big_dict = dict.fromkeys(all_colls)
  for coll in all_colls:
    big_dict[coll] = db.get_all_movies_in_collection(coll)
  return render_template("main.html", iso_dict=big_dict)

@app.route("/search")
def searchmovie():
  searchString = request.args.get("searchwords")
  print "searching for: " + searchString
  searchResultsObj = tmdb.Search().movies(urllib.quote(searchString))

  #if searchResultsObj["total_results"] == 0:
  #  return json.dumps({"results": ""})

  print "total: " + str(searchResultsObj["total_results"])

  # Depaginate
  #searchResults = []
  #for page in searchResultsObj["results"]:
  #  searchResults.append(page)
  searchResults = searchResultsObj["results"]
  
  searchResultsSerializable = []
  for movie in searchResults:
    print "  found: " + movie["title"]
    thisMovie = {}
    thisMovie["title"] = movie["title"]
    thisMovie["year"] = movie["release_date"][:4]
    thisMovie["id"] = movie["id"]
    searchResultsSerializable.append(thisMovie)
  return json.dumps({"results": searchResultsSerializable})

@app.route("/imdbLink")
def imdblink():
  movieId = request.args.get("mid")
  imdbId = tmdb.Movie(movieId).get_imdb_id()
  return json.dumps({"imdbid": imdbId})

@app.route("/rename")
def renameiso():
  pass

#  isoType = request.args.get("type")
#  isoFile = request.args.get("iso")
#  newName = request.args.get("newname")
#  
#  # Get path
#  if (isoType == "dvd"):
#    pathPrefix = "movies/iso/sd/"
#  elif (isoType == "bd"):
#    pathPrefix = "movies/iso/bd/"
#  else:
#    return json.dumps({"error":"Invalid type {0}".format(isoType)})
#
#  # Make sure the source file exists
#  try:
#    with open(pathPrefix + isoFile): pass
#  except IOError:
#    return json.dumps({"error":"File {0} does not exist!".format(pathPrefix + isoFile)})
#
#  # Get rid of invalid characters in the name
#  newName = re.sub("<3", "HEART", newName)
#  newName = re.sub("[<>:\"/\\|\?\*]", "", newName)
#  newName = re.sub("&", "and", newName)
#
#  # Make sure the destination file does not already exist
#  newNameComplete = pathPrefix + newName + ".iso"
#  exists = True
#  try:
#    with open(newNameComplete): pass
#  except IOError:
#    exists = False
#
#  if exists:
#    return json.dumps({"error":"Destination filename {0} already exists!  Not renaming.".format(newNameComplete)})
#
#  os.rename(pathPrefix + isoFile, newNameComplete)
#  return json.dumps({})

@app.route("/remove")
def removeiso():
  pass

if __name__ == "__main__":
  # Get API key from file, Configure TMDB API
  apiKeyFile = open('tmdb.api.key', 'r')
  tmdbApiKey = apiKeyFile.read().strip()
  tmdb.API_KEY = tmdbApiKey

  # Init big data structure from db
  db = FaceDB("sql/face.db")
  all_colls = db.get_all_collections()
  
  # We set iptables to redirect port 80 requests to port 5000, so the default port is ok here
  app.run(host="0.0.0.0", debug=True)
