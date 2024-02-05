from pydantic import BaseModel, Field


class MatchBase(BaseModel):
    """
    BaseModel of Match
    """
    left_player_name: str | None = Field(default=None, description="player name in match", examples=["Daniel"])
    right_player_name: str | None = Field(default=None, description="player name in match", examples=["Silvério"])
    winner: str | None = Field(default=None, description="winning player name", examples=["Daniel"])
    loser: str | None = Field(default=None, description="loser player name", examples=["Silvério"])
    final_match: bool = Field(default=False, description="indicator if it is the final match", examples=[False])
    third_place: bool = Field(default=False, description="indicator if it is the third place match", examples=[False])
    left_previous_match_id: int | None = Field(default=None, description="id of the previous match", examples=[1])
    right_previous_match_id: int | None = Field(default=None, description="id of the previous match", examples=[1])

class MatchCreate(MatchBase):
    """
    BaseModel of Match to create
    """
    pass

class MatchSchema(MatchBase):
    """
    BaseModel of Match to Schema
    """
    id: int = Field(description="id of match", examples=[1])
    tournament_id: int= Field(description="id of tournament", examples=[1])

    class ConfigDict:
        orm_mode = True
