from datetime import datetime

from user.user_status import UserStatus
from utils.utils import Utils

class User:
    def __init__(self, first_name: str,
                 last_name: str) -> None:
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.user_name: str = ''
        self.email: str = ''
        self.password: str = ''
        self.mobile_no: str = ''
        self.date_of_birth: datetime = ''
        self.account_creation_date: int = Utils.getEpoch()
        self.account_status: str = UserStatus.CREATED 
        self.role_id: int = 4
        
    def __str__(self) -> str:        
        return "First Name=" + self.first_name + ", Last Name=" + self.last_name \
            +", email=" + self.email
