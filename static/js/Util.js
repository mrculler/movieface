// Utility functions
// If I were using JS libs, these would not need to be implemented.

function isEmptyObject(obj) {
  if ((obj == null) || (typeof obj != "object")) {
    return false;
  }
  for (var dontcare in obj) {
    // If nonempty
    return false;
  }
  return true;
};
