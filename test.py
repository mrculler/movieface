from facedb import FaceDB
from face_types import Collection, Movie

f=FaceDB('sql/face.db')

all_colls = f.get_all_collections()
big_dict = dict.fromkeys(all_colls)

for coll in all_colls:
  print type(coll)
  big_dict[coll] = f.get_all_movies_in_collection(coll)

for i in big_dict.iterkeys():
  print i
  print len(big_dict[i])

