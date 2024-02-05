from sqlalchemy.orm import Session
from app.src.models.tournament import Tournament
from app.src.schemas.tournament import TournamentCreate


def get_tournament(db: Session, tournament_id: int) -> Tournament:
    """
    Get tournament by id
    :params db: Session
    :params tournament_id:int

    :return Tournament()
    """
    return db.query(Tournament).filter(Tournament.id == tournament_id).one()


def create_tournament(db: Session, tournament: TournamentCreate) -> Tournament:
    """
    Create tournament
    :params db: Session
    :params tournament: TournamentCreate

    :return Tournament()
    """
    db_tournament = Tournament(name=tournament.name)
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament


def get_top_of_tournament(db: Session, tournament_id: int) -> dict[str, str]:
    """
    Return the top four in the tournament if it is closed
    :params db: Session
    :params tournament_id:int

    :return dict[position: str, player_name: str]
    """
    tournament = get_tournament(db, tournament_id)
    final_match = next(match for match in tournament.matchs if match.final_match)
    third_place_match = next((match for match in tournament.matchs if match.third_place), None)
    if (final_match.winner is None or (third_place_match is not None and third_place_match.winner is None)):
        raise Exception("Torneio não finalizado")

    return {
        "Primeiro": final_match.winner,
        "Segundo": final_match.loser,
        "Terceiro": third_place_match.winner if third_place_match is not None else None,
        "Quarto": third_place_match.loser if third_place_match is not None else None
    }
