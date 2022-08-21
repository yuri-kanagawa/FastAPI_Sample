from passlib.context import CryptContext

class Hash():

    def __init__(self):
        self.pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def get_password_hash(self,password):
        return self.pwd_cxt.hash(password)

    def verify_password(self,hashed_password, plain_password):
        return self.pwd_cxt.verify(plain_password, hashed_password)