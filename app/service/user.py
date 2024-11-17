from http import HTTPStatus
from fastapi import HTTPException

from dao.user import UserDAO

from model.user import UserBase
class User:
   @staticmethod
   async def create_user(user: UserBase):
      return await UserDAO.insert(user)

   @staticmethod
   async def get_user_by_email(email: str):
       user_data = await UserDAO.get_by_email(email)
       if not user_data:
           raise HTTPException(HTTPStatus.NOT_FOUND, 'User not found')
       return user_data
   
   @staticmethod
   async def get_users_by_orgid(orgid: int):
       user_data = await UserDAO.get_by_orgid(orgid)
       if not user_data:
           raise HTTPException(HTTPStatus.NOT_FOUND, 'User not found')
       return user_data

   @staticmethod
   async def get_user_by_id(id: int):
      return await UserDAO.get(id)
   
   @staticmethod
   async def exists(email: str):
      return await UserDAO.exists(email)
   
   @staticmethod
   async def delete_user(id: int, orgid: int):
       return await UserDAO.delete(id, orgid)
   
   @staticmethod
   async def update_user(user: UserBase):
       return await UserDAO.update(user)
   
   @staticmethod
   async def self_update_user(user: UserBase):
       return await UserDAO.self_update(user)