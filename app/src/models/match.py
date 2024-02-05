from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.src.core.database import Base


class Match(Base):
    __tablename__ = "matchs"

    id: Mapped[int] = mapped_column(primary_key=True)
    left_player_name: Mapped[str | None]
    right_player_name: Mapped[str | None]
    winner: Mapped[str | None]
    loser: Mapped[str | None]
    loser: Mapped[str | None]
    final_match: Mapped[bool]
    third_place: Mapped[bool]

    left_previous_match_id: Mapped[int | None] = mapped_column(ForeignKey("matchs.id"))
    left_previous_match: Mapped["Match"] = relationship("Match", foreign_keys=[left_previous_match_id])

    right_previous_match_id: Mapped[int | None] = mapped_column(ForeignKey("matchs.id"))
    right_previous_match: Mapped["Match"] = relationship("Match", foreign_keys=[right_previous_match_id])

    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"))
    tournament: Mapped["Tournament"] = relationship(back_populates="matchs")

    def __repr__(self):
        return f"""
            Match(id={self.id},
            left_player_name={self.left_player_name},
            right_player_name={self.right_player_name},
            winner={self.winner},
            loser={self.loser},
            final_match={self.final_match},
            third_place={self.third_place},
            left_previous_match_id={self.left_previous_match_id},
            right_previous_match_id={self.right_previous_match_id})
        """
