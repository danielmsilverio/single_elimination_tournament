from app.src.models.match import Match
from sqlalchemy import or_


class UpdaterWinner:
    """
    Class responsible for performing winner update logic
    """

    def updater_to_winner(self, db, match: Match, winner: str) -> Match:
        """
        Function to perform the necessary updates,
        i.e. updating the winner and loser of the
        match and also in the next matches.

        :params db: Session
        :params match: Match
        :params winner: str

        return Match()
        """
        next_matchs: list[Match] = db.query(Match).filter(or_(Match.left_previous_match_id == match.id,
                                                              Match.right_previous_match_id == match.id)).all()

        match.winner = winner
        match.loser = match.left_player_name if match.left_player_name != winner else match.right_player_name
        db.add(match)

        if (len(next_matchs) == 1):
            next_match = next_matchs[0]
            db.add(self.update_name_match(match.winner, match.id, next_match))
        elif (len(next_matchs) > 1):
            final_match = next(next_match for next_match in next_matchs if next_match.final_match)
            third_place_match = next(next_match for next_match in next_matchs if next_match.third_place)

            final_match = self.update_name_match(match.winner, match.id, final_match)
            third_place_match = self.update_name_match(match.loser, match.id, third_place_match)

            if (third_place_match.left_previous_match_id is None or third_place_match.right_previous_match_id is None):
                third_place_match.winner = match.loser

            db.add(final_match)
            db.add(third_place_match)

        db.commit()
        db.refresh(match)
        return match

    def update_name_match(self, name_update: str, match_id: int, match: Match) -> Match:
        """
        Auxiliary function for updating match names

        :params name_update: str
        :params match_id: int
        :params match: Match

        return Match()
        """
        match.left_player_name = name_update if match.left_previous_match_id == match_id else match.left_player_name
        match.right_player_name = name_update if match.right_previous_match_id == match_id else match.right_player_name
        return match
