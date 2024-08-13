import jwt

data = {
    'name': 'João Victor Cordeiro',
    'email': 'joaocordeiro2134@gmail.com'    
}

encoded_jwt = jwt.encode(data, "l5eOt22JB(F[?&A5i+*QqvrzwhaGVB7)fYeyDLq=", algorithm="HS256")

print(encoded_jwt)