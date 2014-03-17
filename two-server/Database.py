from google.appengine.ext import ndb

class UserList(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    userName = ndb.StringProperty()
    userAlgorithm = ndb.StringProperty(indexed=False)
    userSecretKey = ndb.StringProperty(indexed=False)

