from fastapi import FastAPI
from user.database import db
from user import schema as schemas
from uuid import UUID, uuid4
from user.config import settings
from typing import Dict, List, Optional
import json
import jwt
import bcrypt

app = FastAPI()

class User:
    data: schemas.UserPrivate
    is_new: bool = True

    def __init__(self,
                 id: Optional[UUID] = None,
                 user_data: schemas.PatchUser = {}
                ):
        self._collection = db.collection("user")
        if not id:
            user_id = uuid4()
            self.data = schemas.UserPrivate(id=user_id)
            self.update(dict(user_data))
        
        else:
            try:
                self.data = self.load(id)
            
            except Exception as e:
                print(e)
    
    def save(self):
        data = json.loads(schemas.UserPrivate.parse_obj(self.data).json())
        data["_key"] = data["id"]
        if self.is_new:
            data["password"] = self.hash_password(data["password"])
            self._collection.insert(data)

        else:
            self._collection.replace(data)

    def load(self, id: UUID):
        try:
            user = self._collection.get(str(id))
            if not user:
                raise ValueError
            
            self.is_new = False
            return schemas.UserPrivate.parse_obj(user)
        
        except Exception as e:
            print(e)

    def update(self, data: Dict):
        for item in data:
            try:
                if data[item] != "" and data[item] != None:
                    setattr(self.data, item, data[item])
                    if item == "password":
                        setattr(self.data, item, str(self.hash_password(data[item])))
                        print(str(hash_password(data[item])))
            
            except Exception as e:
                print(e)
        
        self.save()
    
    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
    
    def check_password(self, plain_password: str) -> bool:
        data = json.loads(schemas.UserPrivate.parse_obj(self.data).json())
        return bcrypt.checkpw(plain_password.encode('utf-8'), str(data["password"]).encode('utf-8'))

    def create_token(self):
        token = jwt.encode(payload={'sub': str(self.data.id), 'name': self.data.first_name, 'last_name': self.data.last_name}, key=settings.SECRET, algorithm='HS256')
        return token

    @staticmethod
    def check_token(token):
        try:
            payload = jwt.decode(jwt=token, key=settings.SECRET, algorithms=['HS256', 'RS256'])
            return True
        except:
            return False

    @classmethod
    def by_email(cls, email: str):
        try:
            document = db.collection("user").find({"email": str(email)}).pop()
            print(f"!!!!!!{document}")
            return cls(UUID(document.get("_key")))
        
        except Exception as e:
            print(e)
    
    @classmethod
    def by_id(cls, id: str):
        try:
            document = db.collection("user").find({"id": str(id)}).pop()
            print(f"!!!!!!{document}")
            return cls(UUID(document.get("_key")))
        
        except Exception as e:
            print(e)
