from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    description: str


class HotelPATCH(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)