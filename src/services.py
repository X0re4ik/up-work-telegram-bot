

from typing import Dict, List, Optional
from urllib.error import HTTPError

import aiohttp
from pydantic import BaseModel


class UserAccount(BaseModel):
    telegram_id: int
    security_token: str
    user_uid: str
    org_uid: str
    questions: List[str]
    
    @classmethod
    def from_json(cls, data):
        return cls(
            telegram_id=data["telegram_id"],
            security_token=data["security_token"],
            user_uid=data["user_uid"],
            org_uid=data["org_uid"],
            questions=list(
                map(
                    lambda question_obj: question_obj["question"],
                    data["questions"]
                )
            )
        )


class UserUpdate(BaseModel):
    security_token: Optional[str] = None
    user_uid: Optional[str] = None
    org_uid: Optional[str] = None
    

class QuestionGetModel(BaseModel):
    user_id: int
    question: str
    
    @classmethod
    def from_json(cls, data):
        return cls(
            user_id=data["user_id"],
            question=data["question"]
        )


class AccountTelegramCreate(BaseModel):
    telegram_id: int
    security_token: str
    user_uid: str
    org_uid: str

class ErrorModel(BaseModel):
    code: int
    description: str = ""

class BackendUserService:
    
    def __init__(self, base_url: str, default_path = 'api/v1') -> None:
        self.base_url = base_url
        self.default_path = default_path
        
        self.default_full_path = self.base_url + "/" + self.default_path
        self.base_question_url = self.default_full_path + "/question"
        self.base_account_url = self.default_full_path + "/account"


    async def is_valid(self, telegram_id: int):
        try:
            await self.get_account(telegram_id)
            return True
        except HTTPError as e:
            return False


    async def create_account(self, model: AccountTelegramCreate):
        url = self.base_account_url + "/"
        return await self._run_http_method(url, "post", 201, json=model.model_dump())


    async def get_account(self, telegram_id: int):
        url = self.base_account_url + f"/{telegram_id}/"
        return await self._run_http_method(url, "get", 200)


    async def update_account(self, telegram_id: int, model: UserUpdate):
        url = self.base_account_url + f"/{telegram_id}/"
        return await self._run_http_method(url, "patch", 200, json=model.model_dump())


    async def delete_account(self, telegram_id: int):
        url = self.base_account_url + f"/{telegram_id}/"
        return await self._run_http_method(url, "delete", expected_code=204)


    async def add_question(self, telegram_id: int, question: str):
        url = self.base_question_url + f"/{telegram_id}/"
        return await self._run_http_method(url, "post", 201, json={
            "question": question
        })


    async def get_questions(self, telegram_id: int):
        url = self.base_question_url + f"/{telegram_id}/"
        return await self._run_http_method(url, "get", 200)


    async def delete_questions(self, telegram_id: int, question: str):
        url = self.base_question_url + f"/{telegram_id}/?question={question}"
        return await self._run_http_method(url, "delete", 204)
    
    async def delete_all_questions(self, telegram_id: int):
        url = self.base_question_url + f"/{telegram_id}/"
        return await self._run_http_method(url, "delete", 204)


    async def _run_http_method(self, url, method, expected_code: int = 200, *args, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with getattr(session, method)(url, ssl=False, *args, **kwargs) as response:
                if response.status != expected_code: 
                    raise HTTPError(
                        url=url,
                        code=response.status, 
                        msg=f"{response.status} != {expected_code}",
                        hdrs=response.headers,
                        fp=None
                    )
                if expected_code == 204:
                    return {}
                return await response.json()


api_service = BackendUserService("http://localhost:8000")
            

class TelegramUserService:
    
    def __init__(self, api_service: BackendUserService) -> None:
        self.api_service =api_service
    
    async def is_valid_user(self, telegram_id: int) -> bool:
        return await self.api_service.is_valid(telegram_id)
    
    async def create_account(self, 
                     telegram_id: int, 
                     security_token: str, 
                     user_uid: str, 
                     org_uid: str):
        model = AccountTelegramCreate(
            telegram_id=telegram_id, 
            security_token=security_token, 
            user_uid=user_uid, 
            org_uid=org_uid, 
        )
        data = await self.api_service.create_account(model)
        return UserAccount.from_json(data)
    
    async def get_account(self, telegram_id: int):
        try:
            data = await self.api_service.get_account(telegram_id)
            print(data)
            return UserAccount.from_json(data)
        except HTTPError as e:
            return None
    
    async def update_account(self, 
                             telegram_id: int, 
                             security_token: str,
                             user_uid: str,
                             org_uid: str):
        model = UserUpdate(
            security_token=security_token, 
            user_uid=user_uid, 
            org_uid=org_uid
        )
        data = await self.api_service.update_account(telegram_id, model)
        return UserAccount.from_json(data)
    
    async def delete_account(self, telegram_id: int):
        return await self.api_service.delete_account(telegram_id)
    
    async def get_questions(self, telegram_id: int) -> List[str]:
        data = await self.api_service.get_questions(telegram_id)
        return list(
            map(
                lambda element: element["question"],
                data    
            )
        )
    
    async def add_question(self, telegram_id: int, question: str):
        data = await self.api_service.add_question(telegram_id, question)
        return await self.get_questions(telegram_id)
    
    async def delete_questions(self, telegram_id: int, question: str):
        data = await self.api_service.delete_questions(telegram_id, question)
        return data
    
    async def delete_all_questions(self, telegram_id: int):
        data = await self.api_service.delete_all_questions(telegram_id)
        return data
    
telegram_user_service = TelegramUserService(
    api_service=api_service
)