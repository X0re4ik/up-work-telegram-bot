from typing import Optional, List

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



class NumberQuestions(BaseModel):
    occupied: int
    max_limit: int
    free: int
    