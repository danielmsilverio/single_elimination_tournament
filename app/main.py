from fastapi import Depends, FastAPI, Body
from http import HTTPStatus
from sqlalchemy.orm import Session

from app.src.crud import match as match_crud, tournament as tournament_crud
from app.src.schemas import match, tournament
from app.src.core.database import SessionLocal


app = FastAPI(
    title="Sistema de torneio por chaves eliminatórias",
    description="Projeto para o processo seletivo da Moray"
)


def get_db() -> Session:
    """
    Get session to connect database.
    """
    db: Session = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.get("/", summary="Boas vindas", description="Apenas uma rota de boas vindas")
def home():
    return {"message": "Hello World"}


@app.post("/tournament",
          response_model=tournament.TournamentSchema,
          status_code=HTTPStatus.CREATED,
          description="Criação de um novo torneio e retorna a sua estrutura",
          summary="Criação de um novo torneio")
def create_tournament(tournament: tournament.TournamentCreate, db: Session = Depends(get_db)):
    return tournament_crud.create_tournament(db=db, tournament=tournament)


@app.post("/tournament/{tournament_id}/competitor",
          response_model=list[match.MatchSchema],
          status_code=HTTPStatus.CREATED,
          description="Adiciona os competidores e já cria todas as partidas que a competição terá",
          summary="Adiciona os competidores e cria as partidas")
def add_competitors(tournament_id: int, players: list[str], db: Session = Depends(get_db)):
    return match_crud.batch_tournament_matchmaking(db=db, tournament_id=tournament_id, players=players)


@app.get("/tournament/{tournament_id}/match",
         response_model=list[match.MatchSchema],
         description="Informa uma lista de todas as partidas do torneio",
         summary="Lista das partidas do torneio")
def show_match(tournament_id: int, db: Session = Depends(get_db)):
    return match_crud.get_matchs_by_tournameent(db=db, tournament_id=tournament_id)


@app.post("/tournament/match/{match_id}",
          response_model=match.MatchSchema,
          description="Realiza a atualização do vencedor de uma partida e das próximas se necessário",
          summary="Atualiza o vencedor de uma partida")
def update_match_winner(match_id: int, winner: str = Body(), db: Session = Depends(get_db)):
    return match_crud.update_match_winner(db=db, match_id=match_id, winner=winner)


@app.get("/tournament/{tournament_id}/result",
         response_model=dict[str, str],
         description="Retorna um dicionário com as primeiras quatro posições do torneio se concluído",
         summary="Retorna os primeiros colocados do torneio")
def show_result_by_tournament(tournament_id: int, db: Session = Depends(get_db)):
    return tournament_crud.get_top_of_tournament(db=db, tournament_id=tournament_id)
