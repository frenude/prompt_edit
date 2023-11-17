from typing import Optional, List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    name: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    hometown: Optional[str]
    graduate: Optional[bool]
    education: Optional[str]
    current_residence: Optional[str]
    sexual_orientation: Optional[str]
    work: Optional[str]
    single: Optional[str]
    personality_traits: Optional[List[str]]
    hobby: Optional[List[str]]
    disinterest: Optional[List[str]]
    height: Optional[int]
    weight: Optional[int]
    skin_color: Optional[str]
    hair: Optional[str]
    facial_features: Optional[List[str]]
    physique: Optional[List[str]]
    dressing_style: Optional[str]
    social_relationship: Optional[List[str]]
    friend_preferences: Optional[List[str]]
    lifestyle: Optional[List[str]]
    constellation: Optional[str]
    mbti: Optional[str]
    recent_status: Optional[List[str]]


class Response(BaseModel):
    code: int
    msg: str
    data: dict


class Request(BaseModel):
    content: List[str]


from portrait.portrait import get_user
import json


@app.post("/portrait", response_model=Response)
def get_user_portrait(req: Request):
    resp = get_user(req.content)
    print(resp)
    return Response(code=1, msg="success", data=json.loads(resp))


if __name__ == '__main__':
    uvicorn.run(app="main:app", host="0.0.0.0", port=9876, reload=True)
