from google.appengine.ext import ndb

class UserList(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    Username = ndb.StringProperty(required = True)
    Password = ndb.StringProperty(required = True)
    SecretKey = ndb.StringProperty(required = True, indexed=False)
    Counter = ndb.StringProperty()
    CounterTime = ndb.DateTimeProperty(auto_now_add=True)
