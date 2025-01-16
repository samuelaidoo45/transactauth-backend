from pydantic import BaseModel

class ExampleSchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True
