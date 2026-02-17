from pydantic import BaseModel, HttpUrl
from datetime import datetime

class URLCreate(BaseModel):
    original_url: HttpUrl

class URLResponse(BaseModel):
    short_url: str

class URLStats(BaseModel):
    original_url: str
    short_code: str
    clicks: int
    created_at: datetime
