from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional


class Item(BaseModel):
    id: int
    reputation: int
    creationdate: str = Field(..., alias='creationdate')
    displayname: str = Field(..., alias='displayname')
    lastaccessdate: str = Field(None, alias='lastaccessdate')
    websiteurl: Optional[str] = Field(None, alias='websiteurl')
    location: Optional[str] = None
    aboutme: Optional[str] = Field(None, alias='aboutme')
    views: int
    upvotes: int
    downvotes: int
    profileimageurl: Optional[HttpUrl] = Field(None, alias='profileimageurl')
    age: Optional[int] = None
    accountid: Optional[int] = Field(None, alias='accountid')


class Root(BaseModel):
    items: List[Item]
