from sqlalchemy.orm import Session
from app.src.models.match import Match
from app.src.schemas.match import MatchCreate
from app.src.crud.generator.match_generator import GenerateMatchs
from app.src.crud.generator.updater_winner import UpdaterWinner


def get_match_by_id(db: Session, match_id: int) -> Match:
    """
    Get match by id

    :params db: Session
    :params match_id: int

    :returns Match()
    """
    return db.query(Match).filter(Match.id == match_id).one()


def get_matchs_by_tournameent(db: Session, tournament_id: int) -> list[Match]:
    """
    Get matchs by tournament id

    :params db: Session
    :params tournament_id: int

    :returns list[Match()]
    """
    return db.query(Match).filter(Match.tournament_id == tournament_id).all()


def create_tournament_matchs(db: Session, match: MatchCreate, tournament_id: int) -> Match:
    """
    Create one match to tournament

    :params db: Session
    :params match: MatchCreate
    :params tournament_id: int

    :returns Match()
    """
    db_match = Match(**match.model_dump(), tournament_id=tournament_id)
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


def batch_tournament_matchmaking(db: Session, tournament_id: int, players: list[str]) -> list[Match]:
    """
    Received a list of playes name and create all matchs to tournament

    :params db: Session
    :params tournament_id: int
    :params players: list[str]

    retunr list[Match()]
    """
    GenerateMatchs(db=db, players=players, tournament_id=tournament_id)
    return get_matchs_by_tournameent(db, tournament_id=tournament_id)


def update_match_winner(db: Session, match_id: int, winner: str) -> Match:
    """
    Update the winner of the match and the next ones if necessary

    :params db: Session
    :params match_id: int
    :params winner: str
    """
    match = get_match_by_id(db=db, match_id=match_id)
    if winner not in [match.left_player_name, match.right_player_name]:
        raise Exception("player does not participate in the match")

    return UpdaterWinner().updater_to_winner(db, match, winner)
