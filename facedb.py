import sqlite3

from face_types import Collection, Movie

class FaceDB:
  '''
  SELECT
  '''
  def get_all_collections(self):
    cursor = self.__db.cursor()
    cursor.execute("SELECT * FROM Collections")
    return map(Collection._make, cursor.fetchall())

  def get_all_movies_in_collection(self, collection):
    cursor = self.__db.cursor()
    cursor.execute("SELECT * FROM Movies WHERE collectionId=?", (collection.collection_id,))
    return map(Movie._make, cursor.fetchall())

  '''
  UPDATE
  '''
  def rename_movie(self, movie, new_name):
    cursor = self.__db.cursor()
    cursor.execute("UPDATE Movies SET filename=? AND isRenamed=1 WHERE id=?", (new_name, move_id))
    cursor.commit()

  def set_renamed(self, movie, is_renamed=True):
    renamed_int=1
    if not is_renamed:
      renamed_int=0
    
    cursor = self.__db.cursor()
    cursor.execute("UPDATE Movies SET isRenamed=? WHERE id=?", (renamed_int, movie.movie_id))
    cursor.commit()

  def __init__(self, db_path):
    self.__db = sqlite3.connect(db_path)
