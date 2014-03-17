import json, webapp2
from Database import UserList

class RegisterHandler(webapp2.RequestHandler):
    def get(self):
        self.denyIllegalAccess('Method Not Allowed')
    def post(self):
        # Get parameters from request.
        userName = self.request.get("user",None)
        algorithm = self.request.get("algorithm",None)
        secretKey = self.request.get("secret","")
        if self.isParametersLegal(userName, algorithm, secretKey):
            UserList.userName = userName
            UserList.userAlgorithm = algorithm
            UserList.userSecretKey = secretKey
            UserList.put()
            self.setSuccessResponse()

        else:
            self.denyIllegalAccess('Illegal Parameters')
    def isParametersLegal(self, userName, algorithm, secretKey):
        '''Check whether provided parameters legal'''
        # None check: algorithm must be presented.
        if algorithm not in ["HOTP", "TOTP"]:
            return False
        # Length check: userName, provider and secretKey should be >= 4
        if len(userName) < 4 or len(secretKey) < 4:
            return False

    def setSuccessResponse(self):
        self.response.status = 200
        self.response.body = json.dumps({"success": True})
        self.response.content_type = 'application/json'

    def denyIllegalAccess(self, reason):
        self.response.status = 403
        self.response.body = json.dumps({"reason": reason})
        self.response.content_type = 'application/json'



app = webapp2.WSGIApplication([
    ('/userReg', RegisterHandler)
], debug=True)

# def handle_400(request, response, exception):
#     pass

# def handle_500(request, response, exception):
#     pass

# app.error_handlers[400] = handle_400
# app.error_handlers[500] = handle_500