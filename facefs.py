# Defines filesystem operations for movie repos

import os

# Get the full path and filename for a movie
def get_name(collection, movie_source):
  if type(movie_source) is Movie:
    filename = movie_source.filename
  elif type(movie_source) is str:
    filename = movie_source
  else:
    raise TypeError("Invalid type: {0}".format(type(movie_source)))
  return "{0}.{1}".format(os.path.join(collection.path, filename), collection.extension)

# Makes sure paths are real.
# Takes a dictionary of collections => [movies]
# Returns either True for all validation passed, or False and a 
def validate(collections):
  path_err = "Path {0} does not exist"
  file_err = "File {0} does not exist"

  file_errors = []
  for collection, movie in collections:
    # Return immediately on these errors, otherwise we'll get loads of repetition below
    if not os.path.isdir(collection.path):
      return False, [path_err.format(collection.path),]
    if not os.path.isdir(collection.drop_path):
      return False, [path_err.format(collection.drop_path),]
    
    file_path = get_name(collection, movie)
    if not os.path.isfile(file_path):
      file_errors.append(file_err.format(file_path))
  
  if file_errors:
    return False, file_errors
  return [True,]

def get_file_list(collection):
  return sorted(os.listdir(collection.path))

# The arguments here are strings, and the suffix is omitted from the new filename.
def rename_file(collection, movie, new_filename):
  
  # Get rid of invalid characters
  new_filename = re.sub("<3", "HEART", new_filename)
  new_filename = re.sub("[<>:\"/\\|\?\*]", "", new_filename)
  new_filename = re.sub("&", "and", new_filename)

  # Build some paths
  full_current_name = get_name(collection, movie)
  full_new_name = get_name(collection, new_filename)

  # Make sure files exist and do not exist
  if not os.path.isfile(full_current_name):
    return False, "{0} does not exist!".format(full_current_name)
  if os.path.isfile(full_new_name):
    return False, "{0} already exists!".format(full_new_name)

  # Ok, update fs and db
  os.rename(full_current_filename, full_new_filename)
  
  return [True,]

