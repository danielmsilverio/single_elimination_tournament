from fastapi.testclient import TestClient
from unittest import TestCase
from sqlalchemy.orm import Session
from app.main import app
from app.src.crud import tournament
from app.src.crud import match
from app.src.schemas.tournament import TournamentCreate
from app.src.schemas.match import MatchCreate
from app.src.models.tournament import Tournament
from app.src.models.match import Match
import pytest

client = TestClient(app)


@pytest.fixture
def generate_tournament(fake_db: Session) -> Tournament:
    new_tournament = TournamentCreate(name="Novo torneio")
    return tournament.create_tournament(fake_db, new_tournament)


@pytest.fixture
def generate_match(fake_db: Session, generate_tournament) -> Match:
    new_match = MatchCreate(left_player_name="Left Player", right_player_name="Right Player")
    return match.create_tournament_matchs(fake_db, new_match, generate_tournament.id)


@pytest.fixture
def generate_matchs(fake_db: Session, generate_tournament) -> list[Match]:
    list_matchs = []
    for n in range(5):
        new_match = MatchCreate(left_player_name=f"Left Player {n}", right_player_name=f"Right Player {n}")
        list_matchs.append(match.create_tournament_matchs(fake_db, new_match, generate_tournament.id))
    return list_matchs


def test_create_tournament(fake_db: Session):
    response = client.post(
        "/tournament",
        json={"name": "new tournament"}
    )
    assert response.status_code == 201
    tournament_id = response.json()['id']
    result = tournament.get_tournament(fake_db, tournament_id=tournament_id)

    assert result.name == response.json()['name']


def test_list_matchs(generate_tournament, generate_matchs):
    url = f"/tournament/{generate_tournament.id}/match"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == len(generate_matchs)


def test_batch_tournament_matchmaking(generate_tournament):
    url = f"/tournament/{generate_tournament.id}/competitor"
    response = client.post(
        url,
        json=["Daniel", "Mariano", "Silvério", "Rony", "Raphael", "Dudu"]
    )
    assert response.status_code == 201
    assert len(response.json()) == 6


def test_set_winner(generate_match):
    url = f"/tournament/match/{generate_match.id}"
    response = client.post(
        url,
        json=generate_match.left_player_name
    )
    assert response.status_code == 200

    result = response.json()
    assert result["winner"] == generate_match.left_player_name
    assert result["loser"] == generate_match.right_player_name


def test_get_result(fake_db, generate_tournament):
    final_match = MatchCreate(left_player_name="Daniel", right_player_name="Silvério", final_match=True, winner="Daniel", loser="Silvério")
    third_place_match = MatchCreate(left_player_name="Mariano", right_player_name="Rony", third_place=True, winner="Mariano", loser="Rony")
    match.create_tournament_matchs(fake_db, final_match, generate_tournament.id)
    match.create_tournament_matchs(fake_db, third_place_match, generate_tournament.id)

    url = f"/tournament/{generate_tournament.id}/result"
    response = client.get(url)
    assert response.status_code == 200
    result = response.json()
    result_expected = {'Primeiro': 'Daniel', 'Segundo': 'Silvério', 'Terceiro': 'Mariano', 'Quarto': 'Rony'}
    TestCase().assertDictEqual(result_expected, result)
