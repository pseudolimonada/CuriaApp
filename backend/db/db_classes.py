from dataclasses import dataclass
from backend.constants import UserType


@dataclass
class DBUser:
    user_id: int
    email: str
    password: str
    user_type: UserType


# db_order
# db...
