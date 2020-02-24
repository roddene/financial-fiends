import bcrypt
password = "password"
print( bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))

 # bcrypt.gensalt()).decode('utf-8')
