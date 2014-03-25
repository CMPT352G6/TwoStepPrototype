import hmac
import hashlib
import struct
import time
import random
import json
import logging
import webapp2
from Database import UserList

class VerifyHandler(webapp2.RequestHandler):
    def get(self):
        '''Return a json containing counter'''
        # Get password
        username = self.request.get("username","")
        password = self.request.get("password","")
        # Verify username
        if self.isUserExisted(username):
            user = UserList.query(UserList.Username == username).get()
            storedPassword = user.Password
            # Verify password
            if password == storedPassword:
                # Generate a random number for counter.
                randomCounter = random.randrange(10000000,99999999)
                # Save it to user.
                user.Counter = str(randomCounter)
                user.put()
                # Return it to user.
                self.response.status = 200
                self.response.body = json.dumps({"success": True, "counter": randomCounter})
                self.response.content_type = 'application/json'
            else:
                # Any failure will return a message.
                self.setFailResponse("Wrong Username/Password Combination")
        else:
            # Any failure will return a message.
            self.setFailResponse("Wrong Username/Password Combination")
        

    def post(self):
        # Get parameters from request.
        username = self.request.get("username","")
        dynamicCode = int(self.request.get("dynamicCode","0"))
        if self.isUserExisted(username):
            user = UserList.query(UserList.Username == username).get()
            counter = int(user.Counter)
            secret = str(user.SecretKey)
            expectedCode = int(self.HOTP(secret,counter))
            if expectedCode == dynamicCode:
                self.setSuccessResponse()
            else:
                self.setFailResponse('Bad dynamic code')

        else:
            self.setFailResponse('Bad dynamic code')

    def isUserExisted(self, username):
        '''Check whether provided username exists'''
        # Directly try to get one record from ndb.
        # Expected to get None for True
        return UserList.query(UserList.Username == username).get() != None

    def setSuccessResponse(self):
        self.response.status = 200
        self.response.body = json.dumps({"success": True})
        self.response.content_type = 'application/json'

    def setFailResponse(self, reason):
        self.response.status = 403
        self.response.body = json.dumps({"success": False, "reason": reason})
        self.response.content_type = 'application/json'

    def HOTP(self,key, counter, digits=8):
        C_bytes = struct.pack(b"!Q", counter)
        hmac_sha1 = hmac.new(key=key, msg=C_bytes, digestmod=hashlib.sha1).hexdigest()
        return self.truncate(hmac_sha1)[-digits:]

    def truncate(self,hmac_sha1):
        offset = int(hmac_sha1[-1], 16)
        binary = int(hmac_sha1[offset * 2:(offset * 2 + 8)], 16) & 0x7fffffff
        return str(binary)

app = webapp2.WSGIApplication([
    ('/verify', VerifyHandler)
], debug=True)