from datetime import datetime
from dataclasses import dataclass

class User:
    id: int
    first_namee: str
    last_namee: str
    user_name: str
    password: str
    confirm_password: str
    mobile_no: int
    date_of_birth: datetime
    
    