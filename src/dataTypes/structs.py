from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Dict, Union
from pydantic import BaseModel

from datetime import date

import configparser

#
# SCHOOL ENUMS (BLOCK AND NAME) 
#

class SchoolNameMapper(dict):
    def __init__(self):
        super().__init__()
        self.update({
            "NSHS": SchoolName.NEWTON_SOUTH,
            "NNHS": SchoolName.NEWTON_NORTH,
            None: None
        })

class SchoolName(str, Enum):
    NEWTON_SOUTH: str = "NSHS"
    NEWTON_NORTH: str = "NNHS"

class SchoolBlock(str, Enum):
    A: str = "A"
    ADV: str = "ADVISORY"
    B: str = "B"
    C: str = "C"
    D: str = "D"
    E: str = "E"
    F: str = "F"
    G: str = "G"
    EXTRA: str = "EXTRA"

class SchoolBlocksOnDay(Dict[int, SchoolBlock]):
    def __init__(self):
        super().__init__()
        self.update({
            0 : [SchoolBlock.A, SchoolBlock.ADV, SchoolBlock.B, SchoolBlock.C, SchoolBlock.D, SchoolBlock.E],
            1 : [SchoolBlock.A, SchoolBlock.B, SchoolBlock.F, SchoolBlock.G],
            2 : [SchoolBlock.C, SchoolBlock.D, SchoolBlock.E, SchoolBlock.F],
            3 : [SchoolBlock.A, SchoolBlock.B, SchoolBlock.G, SchoolBlock.E],
            4 : [SchoolBlock.C, SchoolBlock.D, SchoolBlock.F, SchoolBlock.G],
            5: [],
            6: []
        })

class Grade(int, Enum):
    NINE: int = 9
    TEN: int = 10
    ELEVEN: int = 11
    TWELEE: int = 12 # KEEP TWELEE, NICE ARTIFACT

class TableColumn(str, Enum):
    POSITION = ["Position",]
    CS_NAME = ["Name",]
    FIRST_NAME = ["First", "First Name"]
    LAST_NAME = ["Last", "Last Name"]
    LENGTH = ["Day",]
    WEEKDAY= ["Day of Week", "DoW", "D o W", "D of Week"]
    NOTE = ["Notes", "Notes to Student"]
    DATE = ["Date",]
     
    def __eq__(self, val):
        if val != "":
            return val in self.__dict__['_value_']
        else:
            return False

    def __hash__(self) -> int:
        return super().__hash__()

class BlockMapper(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update({
            SchoolBlock.A: "A",
            SchoolBlock.ADV: "ADV",
            SchoolBlock.B: "B",
            SchoolBlock.C: "C",
            SchoolBlock.D: "D",
            SchoolBlock.E: "E",
            SchoolBlock.F: "F",
            SchoolBlock.G: "G"
        })
    
class ReverseBlockMapper(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update({
            "A": SchoolBlock.A,
            "ADV": SchoolBlock.ADV,
            "ADVISORY": SchoolBlock.ADV,
            "B": SchoolBlock.B,
            "C": SchoolBlock.C,
            "D": SchoolBlock.D,
            "E": SchoolBlock.E,
            "F": SchoolBlock.F,
            "G": SchoolBlock.G,
            "EXTRA": SchoolBlock.EXTRA,
        })

#
# API ENUMS
#

class ErrorTypeMapper(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update({
            ErrorType.AUTH: "Authentication Error",
            ErrorType.DB: "Database Error",
            ErrorType.PAYLOAD: "Payload Error"
        })

class ErrorType(Enum):
    AUTH = "Authentication Error"
    DB = "Database Error"
    PAYLOAD = "Payload Error"
    def __str__(self) -> str:
        mapper = ErrorTypeMapper()
        return mapper[self]

#
# STUDENT, TEACHER, CLASSTEACHERS(CUSTOM SET), ABSENTTEACHER, AND SCHEDULE OBJECTS
#

@dataclass
class AbsentTeacher:
    teacher: None 
    length: str
    date: str
    note: str

    def __str__(self):
        return f"{self.first} {self.last} {self.length} {self.date} {self.note}"

@dataclass
class SchoologyCreds:
    keys: dict
    secrets: dict

class RawUpdate(BaseModel):
    poster: str
    content: List[str]
    columns: int = None
#
# SESSION AND TOKEN OBJECTS
#
class ListenerStatus():

    # Represents if action has already been done or not
    state_path: str = "src/state.ini"

    absences: bool = False 
    notifications: bool = False
    date: date
    
    def __init__(self, school: SchoolName, date: date = date.today()):
        self.school = school
        self.date = date
        self.absences, self.notifications = self.readState()
    
    def __repr__(self) -> str:
        return f"Statuses: \n\tAbsence: {self.absences}\n\tNotifications: {self.notifications}"

    def readState(self) -> Tuple[bool, bool]:
        absences: bool = False
        notifications: bool = False

        config = configparser.ConfigParser()
        config.read(ListenerStatus.state_path)

        if config[self.school.value]["absences"] == str(self.date):
            absences = True
        
        if config[self.school.value]["notifications"] == str(self.date):
            notifications = True

        return absences, notifications
    
    def updateState(self, absences: bool, notifications: bool):
        
        config = configparser.ConfigParser()
        config.read(ListenerStatus.state_path)
        
        if absences:
            config[self.school.value]["absences"] = str(self.date)

        if notifications:
            config[self.school.value]["notifications"] = str(self.date)
        
        with open(ListenerStatus.state_path, 'w') as config_file:
            config.write(config_file)
    
    def resetState(school: SchoolName):
        config = configparser.ConfigParser()
        config.read(ListenerStatus.state_path)
        
        config[school.value]["absences"] = str(date(year=2022, month=3, day=23))

        config[school.value]["notifications"] = str(date(year=2022, month=3, day=23))
        
        with open(ListenerStatus.state_path, 'w') as config_file:
            config.write(config_file)
        
    def resetAll():
        for school in SchoolName:
            ListenerStatus.resetState(school)
        
        
        

class ColumnMap(Dict[TableColumn, Tuple[int, int]]):
    def __init__(self):
        super().__init__()
        self.update({
            TableColumn.POSITION: (-1, -1),
            TableColumn.CS_NAME: (-1, -1),
            TableColumn.FIRST_NAME: (-1, -1),
            TableColumn.LAST_NAME: (-1, -1),
            TableColumn.LENGTH: (-1, -1),
            TableColumn.WEEKDAY: (-1, -1),
            TableColumn.NOTE: (-1, -1),
            TableColumn.DATE: (-1, -1),
            "CS_MAP": (-1, -1)
        })

class Confidence(BaseModel):
    confidences: dict
    csMap: Union[Tuple, None]

class NotificationBuild(BaseModel):
    uid: str = None
    tid: str = None
    block: SchoolBlock = None
    date: date = None

class NotificationSend(NotificationBuild):
    fcm: str = None
    title: str = None
    body: str = None
    data: dict = None
