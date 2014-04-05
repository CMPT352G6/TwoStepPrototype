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
        '''Verify user, and return a json string containing counter'''
        # Get username and password
        username = self.request.get("username","")
        password = self.request.get("password","")
        # Verify username
        if self.isUserExisted(username):
            user = UserList.query(UserList.Username == username).get()
            storedPassword = user.Password
            # Verify password
            if password == storedPassword:
                # Generate a random number as counter.
                randomCounter = random.randrange(10000000,99999999)
                # Assign counter to the user.
                user.Counter = str(randomCounter)
                user.put()
                # Send counter back to client.
                self.response.status = 200
                self.response.body = json.dumps({"success": True, "counter": randomCounter})
                self.response.content_type = 'application/json'
            else:
                # Send failure message.
                self.setFailResponse("Wrong Username/Password Combination")
        else:
            # Send failure message.
            self.setFailResponse("Wrong Username/Password Combination")
        

    def post(self):
        '''Verify user and dynamic code, and return a json string indicating result.'''
        # Get username and dynamic code from request.
        username = self.request.get("username","")
        # Try to parse dynamic code. Return error message if parse failed.
        try:
            dynamicCode = int(self.request.get("dynamicCode","0"))
        except ValueError, e:
            self.setFailResponse('Unable to parse dynamic code to integar')
            return
        
        # Verify username
        if self.isUserExisted(username):
            user = UserList.query(UserList.Username == username).get()
            # Get key and counter 
            counter = int(user.Counter)
            secret = str(user.SecretKey)
            # Calcuate dynamic code
            expectedCode = int(self.HOTP(secret,counter))
            # Verify dynamic code
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
        '''Set success response'''
        self.response.status = 200
        self.response.body = json.dumps({"success": True})
        self.response.content_type = 'application/json'

    def setFailResponse(self, reason):
        '''Set failure response'''
        self.response.status = 403
        self.response.body = json.dumps({"success": False, "reason": reason})
        self.response.content_type = 'application/json'

    def HOTP(self,key, counter, digits=8):
        '''Compute OTP'''
        # Convert key to byte array
        C_bytes = struct.pack(b"!Q", counter)
        # Compute and return OTP
        hmac_sha1 = hmac.new(key=key, msg=C_bytes, digestmod=hashlib.sha1).hexdigest()
        return self.truncate(hmac_sha1)[-digits:]

    def truncate(self,hmac_sha1):
        '''Dynamically select 4 bytes from SHA-1 value by its last byte.'''
        offset = int(hmac_sha1[-1], 16)
        binary = int(hmac_sha1[offset * 2:(offset * 2 + 8)], 16) & 0x7fffffff
        return str(binary)

app = webapp2.WSGIApplication([
    ('/verify', VerifyHandler)
], debug=True)