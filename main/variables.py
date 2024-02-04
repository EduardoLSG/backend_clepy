from enum import Enum

DECIMAL_PLACES_FIELD = 3
MAX_DIGITS_FIELD = 9

class StatusProductEnum(Enum):
    WAITING     = '0'
    APPROVED    = '1'
    DISAPPROVED = '2' 


choices_status = ((s.value, s.name) for s in StatusProductEnum)