from pydantic.dataclasses import dataclass
from typing import List, Optional

@dataclass
class UserItem:
	username: str
	first_name: str
	last_name: str
	phone_number: Optional[int] = None
	email: Optional[str] = None
	adress: Optional[str] = None

@dataclass
class UserList:
	status_code: int
	message: str
	items: List[UserItem]

@dataclass
class UserOperations:
	status_code: int
	message: str