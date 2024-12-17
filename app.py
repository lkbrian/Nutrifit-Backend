from config import app
from config import api
from routes import CreateAccount,VerifyAccount,Login,Logout,Home




api.add_resource(Home, '/')
api.add_resource(CreateAccount, '/create_account')
api.add_resource(VerifyAccount, '/verify_account')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')


if __name__ == "__main__":
    app.run(port=5555, debug=True)

