import hmac
import hashlib
import array
import time

class VerifyHandler(webapp2.RequestHandler):
    def get(self):
        self.denyIllegalAccess('Method Not Allowed')
    def post(self):
        # Get parameters from request.
        user = self.request.get("user",None)
        algorithm = self.request.get("algorithm",None)
        counter = self.request.get("counter","")
        OTP = self.request.get("otp","")
        if self.isParametersLegal(user, algorithm, counter, OTP):
            query = UserList.query(UserList.userName == user)
            secret = query.get().userSecretKey
            if algorithm == "HOTP":
                userPassword = self.HOTP(secret, counter)
                if otp == userPassword:
                    self.setSuccessResponse()
                else:
                    self.setFailResponse()
            else if algorithm == "TOTP":
                userPassword = self.TOTP(secret, counter)
                if otp == userPassword:
                    self.setSuccessResponse()
                else:
                    self.setFailResponse()
            else:
                denyIllegalAccess('Bad Password')

        else:
            self.denyIllegalAccess('Illegal Parameters')

    def isParametersLegal(self, userName, algorithm, counter, otp):
        '''Check whether provided parameters legal'''
        # None check: algorithm must be presented.
        if algorithm not in ["HOTP", "TOTP"]:
            return False
        # Length check: userName >= 4, counter >= 10
        if len(userName) < 4 or len(counter) < 10:
            return False
        if otp != 8:
            return False

    def setSuccessResponse(self):
        self.response.status = 200
        self.response.body = json.dumps({"success": True})
        self.response.content_type = 'application/json'

    def denyIllegalAccess(self, reason):
        self.response.status = 403
        self.response.body = json.dumps({"reason": reason})
        self.response.content_type = 'application/json'

    def setFailResponse(self):
        self.response.status = 403
        self.response.body = json.dumps({"success": False})
        self.response.content_type = 'application/json'

    def HOTP(K, C, digits=8):
        C_bytes = _long_to_byte_array(C)
        hmac_sha1 = hmac.new(key=K, msg=C_bytes,
                             digestmod=hashlib.sha1).hexdigest()
        return Truncate(hmac_sha1)[-digits:]

    def Truncate(hmac_sha1):
        offset = int(hmac_sha1[6], 16)
        binary = int(hmac_sha1[offset:(offset  + 8)], 16) & 0x7fffffff
        return str(binary)

    def _long_to_byte_array(long_num):
        byte_array = array.array('B')
        for i in reversed(range(0, 8)):
            byte_array.insert(0, long_num & 0xff)
            long_num >>= 8
        return byte_array

app = webapp2.WSGIApplication([
    ('/verify', VerifyHandler)
], debug=True)