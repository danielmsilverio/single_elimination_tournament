from pydantic import BaseModel, Field
from app.src.schemas.match import MatchSchema


class TournamentBase(BaseModel):
    """
    BaseModel of Tournament
    """
    name: str = Field(description="name of tournament", examples=["Nome do torneio"])


class TournamentCreate(TournamentBase):
    """
    BaseModel of Tournament to created
    """
    pass


class TournamentSchema(TournamentBase):
    """
    BaseModel of Tournament to Schema
    """
    id: int = Field(description="id of tournament", examples=[1,2,3])
    matchs: list[MatchSchema] = Field(description="list of Matchs", default=[])

    class ConfigDict:
        orm_mode = True


