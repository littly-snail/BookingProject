from enum import Enum


class Credentials(Enum):
    USERNAME = 'admin'
    PASSWORD = 'password123'

class Timeouts(Enum):
    TIMEOUT = 5

class Ids(Enum):
    id1 = 1
    id2 = 99999