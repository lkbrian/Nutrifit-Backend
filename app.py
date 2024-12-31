from config import app
from config import api
from routes import CreateAccount,VerifyAccount,Login,Logout,Home,Reset_password,Forgot_password,User_Info




api.add_resource(Home, '/')
api.add_resource(User_Info, '/user_info','/user_info/<int:id>')
api.add_resource(CreateAccount, '/create_account')
api.add_resource(VerifyAccount, '/verify_account')
api.add_resource(Reset_password, '/reset_password')
api.add_resource(Forgot_password, '/forgot_password')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

if __name__ == "__main__":
    app.run(port=5555, debug=True, host='0.0.0.0')


