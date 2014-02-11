CREATE TABLE Collections (
  id INTEGER PRIMARY KEY,
  displayName TEXT UNIQUE NOT NULL,
  extension TEXT NOT NULL,
  path TEXT UNIQUE NOT NULL,
  dropPath TEXT UNIQUE NOT NULL
);

CREATE TABLE Movies (
  id INTEGER PRIMARY KEY,
  collectionId INTEGER,
  isRenamed INTEGER NOT NULL,
  filename TEXT NOT NULL,
  CHECK (isRenamed IN (0, 1)),
  UNIQUE (collectionId, filename),
  FOREIGN KEY(collectionId) REFERENCES Collections(id) ON DELETE SET NULL ON UPDATE CASCADE
);
