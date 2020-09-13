from flask_restful import Resource

class SMSCodeResource(Resource):
    '''短信验证码'''
    def get(self):
        return {'get':'foo'}