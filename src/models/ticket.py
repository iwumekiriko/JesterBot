from datetime import datetime
from typing import Optional

from .user import User


class Ticket:
    def __init__(
        self,
        id: Optional[int] = None,
        date_close: Optional[datetime] = None,
        date_create: Optional[datetime] = None,
        description_problem: Optional[str] = None,
        additional_info: Optional[str] = None,
        solution: Optional[str] = None,
        type_problem: Optional[str] = None,
        moderator_id: Optional[int] = None,
        user_id: Optional[int] = None,
        user: Optional[User] = None
    ) -> None:
        self._id = id
        self._date_close = date_close
        self._date_create = date_create
        self._description_problem = description_problem
        self._additional_info = additional_info
        self._solution = solution
        self._type_problem = type_problem
        self._moderator_id = moderator_id
        self._user_id = user_id
        self._user = user
    
    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @id.setter
    def id(self, id: int) -> None:
        self._id = id

    @property
    def date_close(self) -> Optional[datetime]:
        return self._date_close
    
    @property
    def date_create(self) -> Optional[datetime]:
        return self._date_create
    
    @property
    def description_problem(self) -> Optional[str]:
        return self._description_problem
    
    @property
    def additional_info(self) -> Optional[str]:
        return self._additional_info
    
    @property
    def solution(self) -> Optional[str]:
        return self._solution
    
    @solution.setter
    def solution(self, solution: str) -> None:
        self._solution = solution
    
    @property
    def type_problem(self) -> Optional[str]:
        return self._type_problem
 
    @property
    def moderator_id(self) -> Optional[int]:
        return self._moderator_id
    
    @moderator_id.setter
    def moderator_id(self, moderator_id: int) -> None:
        self._moderator_id = moderator_id
   
    @property
    def user_id(self) -> Optional[int]:
        return self._user_id
    
    @property
    def user(self) -> Optional[User]:
        return self._user

    def to_create(self) -> dict:
         return {
            "id": self._id,
            "descriptionProblem": self._description_problem,
            "additionalInfo": self._additional_info,
            "typeProblem": self._type_problem,
            "userId": self._user_id,
        }
    
    def to_start(self) -> dict:
        return {
            "id": self._id,
            "moderatorId": self._moderator_id
        }
    
    def to_close(self) -> dict:
        return {
            "id": self._id,
            "solution": self._solution
        }