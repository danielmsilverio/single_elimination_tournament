from app.src.crud import tournament
from app.src.crud import match
from sqlalchemy.orm import Session
from app.src.schemas.tournament import TournamentCreate
from app.src.schemas.match import MatchCreate
from unittest import TestCase
import pytest


class TestTournaments:
    def test_create_tournament(self, fake_db: Session) -> None:
        new_tournament = TournamentCreate(name="Novo torneio")
        t = tournament.create_tournament(fake_db, new_tournament)
        assert t.name == "Novo torneio"
        assert t.id is not None

    def test_get_tournament(self, fake_db: Session) -> None:
        new_tournament = TournamentCreate(name="Novo torneio")
        t = tournament.create_tournament(fake_db, new_tournament)
        assert t.name == "Novo torneio"
        assert t.id is not None
        result = tournament.get_tournament(fake_db, tournament_id=t.id)
        assert result.name == "Novo torneio"
        assert result.id == t.id

    def test_get_result_without_winner_in_final(self, fake_db: Session) -> None:
        new_tournament = tournament.create_tournament(fake_db, TournamentCreate(name="Novo torneio"))
        final_match = MatchCreate(left_player_name="Daniel", right_player_name="Silvério", final_match=True)
        third_place_match = MatchCreate(left_player_name="Mariano", right_player_name="Rony", third_place=True, winner="Mariano", loser="Rony")
        match.create_tournament_matchs(fake_db, final_match, new_tournament.id)
        match.create_tournament_matchs(fake_db, third_place_match, new_tournament.id)
        with pytest.raises(Exception):
            tournament.get_top_of_tournament(fake_db, new_tournament.id)

    def test_get_result_without_winner_in_third_place(self, fake_db: Session) -> None:
        new_tournament = tournament.create_tournament(fake_db, TournamentCreate(name="Novo torneio"))
        final_match = MatchCreate(left_player_name="Daniel", right_player_name="Silvério", final_match=True, winner="Daniel", loser="Silvério")
        third_place_match = MatchCreate(left_player_name="Mariano", right_player_name="Rony", third_place=True)
        match.create_tournament_matchs(fake_db, final_match, new_tournament.id)
        match.create_tournament_matchs(fake_db, third_place_match, new_tournament.id)
        with pytest.raises(Exception):
            tournament.get_top_of_tournament(fake_db, new_tournament.id)

    def test_get_result_two_players(self, fake_db: Session) -> None:
        new_tournament = tournament.create_tournament(fake_db, TournamentCreate(name="Novo torneio"))
        final_match = MatchCreate(left_player_name="Daniel", right_player_name="Silvério", final_match=True, winner="Daniel", loser="Silvério")
        match.create_tournament_matchs(fake_db, final_match, new_tournament.id)

        result_expected = {"Primeiro": "Daniel", "Segundo": "Silvério", "Terceiro": None, "Quarto": None}
        result = tournament.get_top_of_tournament(fake_db, new_tournament.id)
        TestCase().assertDictEqual(result_expected, result)

    def test_get_result_three_players(self, fake_db: Session) -> None:
        new_tournament = tournament.create_tournament(fake_db, TournamentCreate(name="Novo torneio"))
        final_match = MatchCreate(left_player_name="Daniel", right_player_name="Silvério", final_match=True, winner="Daniel", loser="Silvério")
        third_place_match = MatchCreate(left_player_name="Mariano", right_player_name=None, third_place=True, winner="Mariano")
        match.create_tournament_matchs(fake_db, final_match, new_tournament.id)
        match.create_tournament_matchs(fake_db, third_place_match, new_tournament.id)

        result_expected = {"Primeiro": "Daniel", "Segundo": "Silvério", "Terceiro": "Mariano", "Quarto": None}
        result = tournament.get_top_of_tournament(fake_db, new_tournament.id)
        TestCase().assertDictEqual(result_expected, result)

    def test_get_result_four_players(self, fake_db: Session) -> None:
        new_tournament = tournament.create_tournament(fake_db, TournamentCreate(name="Novo torneio"))
        final_match = MatchCreate(left_player_name="Daniel", right_player_name="Silvério", final_match=True, winner="Daniel", loser="Silvério")
        third_place_match = MatchCreate(left_player_name="Mariano", right_player_name="Rony", third_place=True, winner="Mariano", loser="Rony")
        match.create_tournament_matchs(fake_db, final_match, new_tournament.id)
        match.create_tournament_matchs(fake_db, third_place_match, new_tournament.id)

        result_expected = {"Primeiro": "Daniel", "Segundo": "Silvério", "Terceiro": "Mariano", "Quarto": "Rony"}
        result = tournament.get_top_of_tournament(fake_db, new_tournament.id)
        TestCase().assertDictEqual(result_expected, result)
