import json, webapp2
from Database import UserList

class RegisterHandler(webapp2.RequestHandler):

    def get(self):
        '''Deny GET request.'''
        self.denyIllegalAccess('Method Not Allowed')
    def post(self):
        '''Handle registeration request'''
        # Get parameters from request.
        username = self.request.get("username","")
        password = self.request.get("password","")
        secretKey = self.request.get("serialNumber","")
        # Add the user's details when no user existed with the same user name.
        if not self.isUserExisted(username):
            user = UserList()
            user.Username = username
            user.Password = password
            user.SecretKey = secretKey
            user.put()
            self.setSuccessResponse()

        # Deny registering when a duplicated user is found.
        else:
            self.denyIllegalAccess('Username Existed')
    def isUserExisted(self, username):
        '''Check whether provided username exists'''
        # Directly try to get one record from ndb.
        # Expected to get None for True
        return UserList.query(UserList.Username == username).get() != None

    def setSuccessResponse(self):
        '''Set success response'''
        self.response.status = 200
        self.response.body = json.dumps({"success": True})
        self.response.content_type = 'application/json'

    def denyIllegalAccess(self, reason):
        '''Set failure response'''
        self.response.status = 403
        self.response.body = json.dumps({"success": False, "reason": reason})
        self.response.content_type = 'application/json'



app = webapp2.WSGIApplication([
    ('/register', RegisterHandler)
], debug=True)