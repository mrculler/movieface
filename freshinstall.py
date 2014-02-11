import sqlite3

db_connection = sqlite3.connect("mf.db")

def import_library(directory):
  for movie_file in os.listdir(directory):
    esc_file = movie_file.
    insert_statement = "INSERT INTO Movies (collectionId, isRenamed, filename) VALUES (1, 0, {0});".format(movie_file)
    
def init_db(movie_root):
  
