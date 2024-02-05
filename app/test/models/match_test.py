from app.src.crud import match
from app.src.crud import tournament
from sqlalchemy.orm import Session
from app.src.models.tournament import Tournament
from app.src.schemas.tournament import TournamentCreate
from app.src.schemas.match import MatchCreate
import pytest


class TestMatch:

    @pytest.fixture
    def get_tournament(self, fake_db: Session):
        new_tournament = TournamentCreate(name="Novo torneio")
        return tournament.create_tournament(fake_db, new_tournament)

    @pytest.fixture
    def generate_matchs(self, fake_db: Session, get_tournament: Tournament):
        list_matchs = []
        for n in range(5):
            new_match = MatchCreate(left_player_name=f"Left Player {n}", right_player_name=f"Right Player {n}")
            list_matchs.append(match.create_tournament_matchs(fake_db, new_match, get_tournament.id))
        return list_matchs

    def test_create_match(self, fake_db: Session, get_tournament: Tournament) -> None:
        new_match = MatchCreate(left_player_name="Daniel", right_player_name="Silvério")
        g = match.create_tournament_matchs(fake_db, new_match, get_tournament.id)
        assert g.id is not None
        assert g.left_player_name == "Daniel"
        assert g.right_player_name == "Silvério"

    def test_get_match_by_tournament(self, fake_db: Session, get_tournament: Tournament, generate_matchs: list) -> None:
        matchs = match.get_matchs_by_tournameent(fake_db, get_tournament.id)
        assert len(matchs) == len(generate_matchs)

    def test_batch_tournament_matchmaking_one_player(self, fake_db: Session, get_tournament: Tournament) -> None:
        players = ["Daniel"]
        with pytest.raises(Exception):
            match.batch_tournament_matchmaking(fake_db, get_tournament.id, players)

    def test_batch_tournament_matchmaking_two_players(self, fake_db: Session, get_tournament: Tournament) -> None:
        players = ["Daniel", "Mariano"]
        result = match.batch_tournament_matchmaking(fake_db, get_tournament.id, players)

        assert len(result) == 1
        match_result = result[0]
        assert players[0] in [match_result.left_player_name, match_result.right_player_name]
        assert players[1] in [match_result.left_player_name, match_result.right_player_name]
        assert match_result.final_match

    def test_batch_tournament_matchmaking_three_players(self, fake_db: Session, get_tournament: Tournament) -> None:
        players = ["Daniel", "Mariano", "Silvério"]
        result = match.batch_tournament_matchmaking(fake_db, get_tournament.id, players)

        assert len(result) == 3
        list_names_in_matchs = []
        list_names_in_matchs.extend(g.left_player_name for g in result if g.left_player_name is not None)
        list_names_in_matchs.extend(g.right_player_name for g in result if g.right_player_name is not None)
        for player in players:
            assert player in list_names_in_matchs

    def test_batch_tournament_matchmaking_four_players(self, fake_db: Session, get_tournament: Tournament) -> None:
        players = ["Daniel", "Mariano", "Silvério", "Rony"]
        result = match.batch_tournament_matchmaking(fake_db, get_tournament.id, players)

        assert len(result) == 4
        list_names_in_matchs = []
        list_names_in_matchs.extend(g.left_player_name for g in result if g.left_player_name is not None)
        list_names_in_matchs.extend(g.right_player_name for g in result if g.right_player_name is not None)
        for player in players:
            assert player in list_names_in_matchs

    def test_batch_tournament_matchmaking_six_players(self, fake_db: Session, get_tournament: Tournament) -> None:
        players = ["Daniel", "Mariano", "Silvério", "Rony", "Raphael", "Dudu"]
        result = match.batch_tournament_matchmaking(fake_db, get_tournament.id, players)

        assert len(result) == 6
        list_names_in_matchs = []
        list_names_in_matchs.extend(g.left_player_name for g in result if g.left_player_name is not None)
        list_names_in_matchs.extend(g.right_player_name for g in result if g.right_player_name is not None)
        for player in players:
            assert player in list_names_in_matchs

    def test_batch_tournament_matchmaking_twelve_players(self, fake_db: Session, get_tournament: Tournament) -> None:
        players = ["Daniel", "Mariano", "Silvério", "Rony", "Raphael", "Dudu", "Endrick", "Caio", "Luiz", "Bruno", "Zé", "Mar"]
        result = match.batch_tournament_matchmaking(fake_db, get_tournament.id, players)

        assert len(result) == 12
        list_names_in_matchs = []
        list_names_in_matchs.extend(g.left_player_name for g in result if g.left_player_name is not None)
        list_names_in_matchs.extend(g.right_player_name for g in result if g.right_player_name is not None)
        for player in players:
            assert player in list_names_in_matchs

    def test_update_winnr_with_incorrect_name(self, fake_db: Session, get_tournament: Tournament):
        new_match = MatchCreate(left_player_name="Daniel", right_player_name="Silvério", final_match=True)
        match_created = match.create_tournament_matchs(fake_db, new_match, get_tournament.id)

        with pytest.raises(Exception):
            match.update_match_winner(fake_db, match_created.id, "Mariano")

    def test_update_winner_final_match(self, fake_db: Session, get_tournament: Tournament):
        new_match = MatchCreate(left_player_name="Daniel", right_player_name="Silvério", final_match=True)
        match_created = match.create_tournament_matchs(fake_db, new_match, get_tournament.id)

        match_updated = match.update_match_winner(fake_db, match_created.id, "Daniel")

        assert match_updated.winner == "Daniel"
        assert match_updated.loser == "Silvério"
        assert match_updated.final_match
        assert not match_updated.third_place

    def test_update_winner_third_place_match(self, fake_db: Session, get_tournament: Tournament):
        new_match = MatchCreate(left_player_name="Daniel", right_player_name="Silvério", third_place=True)
        match_created = match.create_tournament_matchs(fake_db, new_match, get_tournament.id)
        match_updated = match.update_match_winner(fake_db, match_created.id, "Daniel")

        assert match_updated.winner == "Daniel"
        assert match_updated.loser == "Silvério"
        assert not match_updated.final_match
        assert match_updated.third_place

    def test_update_match_winner_when_three_players_tournament(self, fake_db: Session, get_tournament: Tournament):
        players = ["Daniel", "Mariano", "Silvério"]
        result = match.batch_tournament_matchmaking(fake_db, get_tournament.id, players)

        normal_match = next(match for match in result if not match.final_match and not match.third_place)
        final_match = next(final_match for final_match in result if final_match.final_match)
        third_place_match = next(third_place_match for third_place_match in result if third_place_match.third_place)

        assert final_match.left_player_name is not None or final_match.right_player_name is not None
        assert third_place_match.left_player_name is None
        assert third_place_match.right_player_name is None

        match_updated = match.update_match_winner(fake_db, normal_match.id, normal_match.left_player_name)

        assert match_updated.winner == normal_match.left_player_name
        assert match_updated.loser == normal_match.right_player_name
        assert not match_updated.final_match
        assert not match_updated.third_place

        fake_db.refresh(final_match)
        fake_db.refresh(third_place_match)

        assert match_updated.winner in [final_match.left_player_name, final_match.right_player_name]
        assert match_updated.loser in [third_place_match.left_player_name, third_place_match.right_player_name]
        assert third_place_match.winner == normal_match.right_player_name == match_updated.loser

    def test_update_match_winner_when_four_players(self, fake_db: Session, get_tournament: Tournament):
        players = ["Daniel", "Mariano", "Silvério", "Rony"]
        result = match.batch_tournament_matchmaking(fake_db, get_tournament.id, players)

        first_match = next(match for match in result if not match.final_match and not match.third_place)
        second_normal_match = next(match for match in result
                                   if not match.final_match and not match.third_place and match.id is not first_match.id)
        final_match = next(final_match for final_match in result if final_match.final_match)
        third_place_match = next(third_place_match for third_place_match in result if third_place_match.third_place)

        assert final_match.left_player_name is None
        assert final_match.right_player_name is None
        assert third_place_match.left_player_name is None
        assert third_place_match.right_player_name is None

        match_updated = match.update_match_winner(fake_db, first_match.id, first_match.left_player_name)

        assert match_updated.winner == first_match.left_player_name
        assert match_updated.loser == first_match.right_player_name

        fake_db.refresh(final_match)
        fake_db.refresh(third_place_match)

        assert match_updated.winner in [final_match.left_player_name, final_match.right_player_name]
        assert match_updated.loser in [third_place_match.left_player_name, third_place_match.right_player_name]
        assert final_match.winner is None
        assert third_place_match.winner is None

        match_updated = match.update_match_winner(fake_db, second_normal_match.id, second_normal_match.left_player_name)

        assert match_updated.winner == second_normal_match.left_player_name
        assert match_updated.loser == second_normal_match.right_player_name

        fake_db.refresh(final_match)
        fake_db.refresh(third_place_match)

        assert match_updated.winner in [final_match.left_player_name, final_match.right_player_name]
        assert match_updated.loser in [third_place_match.left_player_name, third_place_match.right_player_name]
        assert final_match.winner is None
        assert third_place_match.winner is None

    def test_update_simple_match_when_six_players(self, fake_db: Session, get_tournament: Tournament):
        players = ["Daniel", "Mariano", "Silvério", "Rony", "Raphael", "Dudu"]
        result = match.batch_tournament_matchmaking(fake_db, get_tournament.id, players)

        normal_match = next(normal_match for normal_match in result
                            if normal_match.left_player_name is None and normal_match.right_player_name is None)
        final_match = next(final_match for final_match in result if final_match.final_match)
        third_place_match = next(third_place_match for third_place_match in result if third_place_match.third_place)

        assert final_match.left_player_name is None
        assert final_match.right_player_name is None
        assert third_place_match.left_player_name is None
        assert third_place_match.right_player_name is None

        match_updated = match.update_match_winner(fake_db, normal_match.id, normal_match.left_player_name)

        assert match_updated.winner == normal_match.left_player_name
        assert match_updated.loser == normal_match.right_player_name

        fake_db.refresh(final_match)
        fake_db.refresh(third_place_match)

        assert final_match.left_player_name is None
        assert final_match.right_player_name is None
        assert final_match.winner is None
        assert third_place_match.winner is None
