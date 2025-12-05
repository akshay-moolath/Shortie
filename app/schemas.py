from pydantic import BaseModel

class urlshortner(BaseModel):
    id : int
    orginal_url : str
    short_code : str
    class Config:
        from_attributes = True
class URLRequest(BaseModel):
    url: str