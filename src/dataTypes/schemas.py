from sre_constants import SUCCESS
from typing import List, Literal, Optional, Tuple, Union
from uuid import UUID
from pydantic import BaseModel, validator
from ..dataTypes import structs
from datetime import datetime, date

from ..database.database import Base

class UserBase(BaseModel):
    first: str = None
    last: str = None
    school: structs.SchoolName = None
    grade: Literal[9, 10, 11, 12] = None

    def __str__(self) -> str:
        return f"{self.first} {self.last}"
    
    def __hash__(self):
        return hash(str(self.number))

class UserCreate(UserBase):
    gid: str = None

class TeacherCreate(BaseModel):
    first: str = None
    last: str = None
    school: structs.SchoolName = None

    def __repr__(self) -> str:
        return f"{self.first} {self.last}"

class TeacherReturn(TeacherCreate):
    tid: str = None

    class Config:
        orm_mode = True

class Schedule(BaseModel):
    A: List[TeacherReturn] = None
    ADVISORY: List[TeacherReturn] = None
    B: List[TeacherReturn] = None
    C: List[TeacherReturn] = None 
    D: List[TeacherReturn] = None
    E: List[TeacherReturn] = None
    F: List[TeacherReturn] = None
    G: List[TeacherReturn] = None 
    EXTRA: List[TeacherReturn] = None

    @staticmethod
    def scheduleFromList(classes: list):
        schedule = Schedule()
        for cls in classes:
            current = getattr(schedule, cls.block)
            if current != None:
                current.append(cls.teacher)
                setattr(schedule, cls.block, current)
            else:
                setattr(schedule, cls.block, [cls.teacher])
        return schedule

class Class(BaseModel):
    tid: str = None
    block: structs.SchoolBlock = None
    uid: str = None

    class Config:
        orm_mode = True

    def __repr__(self) -> str:
        return f"tid: {self.tid} Block: {self.block} uid: {self.uid}"
    
    # @staticmethod
    # def listFromSchedule(schedule: Schedule, uid: str):
    #     clsList = []
    #     for block in schedule:
    #         for _ in block[1]:
    #             clsList.append(Class(block=ReverseBlockMapper()[block[0]], uid=uid))
    #     return clsList

class TeacherFull(TeacherReturn):
    schedule: List[Class] = []
    
    class Config:
        orm_mode = True

class UserReturn(UserCreate):
    uid: str = None
    schedule: Union[Schedule, List[Class]] = [] 

    class Config:
        orm_mode = True

class SessionCreate(BaseModel):
    uid: Optional[str] = None
    @validator('uid')
    def checkUIDLength(cls, v):
        try:
            UUID(v)
            return v
        except:
            raise ValueError('Invalid UID.')

class SessionReturn(SessionCreate):
    sid: Optional[str] = None
    last_accessed: Optional[datetime] = None

    @validator('sid')
    def checkSIDLength(cls, v):
        if len(v) != 16:
            raise ValueError('SID Must be 17 characters long.')
        return v
    class Config:
        orm_mode = True

class Token(BaseModel):
    token: str

class UserInfo(BaseModel):
    profile: UserBase
    schedule: Schedule
    fcm: Token

class SessionCredentials(BaseModel):
    token: Optional[str] = None
    refresh: Optional[str] = None
    onboarded: Optional[bool] = None

class AbsenceBase(BaseModel):
    length: Optional[str] = None
    note: Optional[str] = None

class AbsenceCreate(AbsenceBase):
    teacher: TeacherCreate
    date: date

    def __repr__(self) -> str:
        return super().__repr__()

class AbsenceReturn(AbsenceBase):
    teacher: TeacherReturn
    date: date

class CanceledClassCreate(Class):
    date: date

    def __repr__(self) -> str:
        return super().__repr__()

class PartialName(BaseModel):
    name: str 
    school: str

    @validator('name')
    def checkPartialName(cls, v):
        if (len(v)) < 3:
            raise ValueError('Phrase too short.')
        return v
        
    @validator('school')
    def checkSchoolName(cls, v):
        if v != ("NNHS" or "NSHS"):
            raise ValueError('Invalid school.')
        return v

class SessionList(BaseModel):
    sessions: List[SessionReturn]

class AbsenceList(BaseModel):
    absences: Tuple

class AutoComplete(BaseModel):
    suggestions: list

class Valid(BaseModel):
    value: bool

class Analytics(BaseModel):
    userCount: int
    totalAbsences: int

class Bool(BaseModel):
    success: bool