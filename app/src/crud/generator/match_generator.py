from app.src.crud.generator.player_match import PlayerMath
from app.src.crud import match
from app.src.schemas.match import MatchCreate
import math


class GenerateMatchs:
    """
    Class responsible for creating the necessary number of matches and distributing participants
    
    :params db: Session
    :params players: list[str]
    :params tournament_id: int
    """
    def __init__(self, db, players: list[str], tournament_id: int) -> None:
        self.__db = db
        self.__players: list[PlayerMath | None] = [PlayerMath(player) for player in players]
        self.__tournament_id = tournament_id
        if len(players) < 2:
            raise Exception("number of participants less than 2")
        elif len(players) == 2:
            left_player = self.__players[0]
            right_player = self.__players[1]
            self.insert_match_create(left_player=left_player, right_player=right_player, final_match=True)
        elif len(players) == 3:
            self.create_match_to_three_players()
        else:
            self.create_all_matchs()

    def insert_match_create(self, left_player: PlayerMath | None, right_player: PlayerMath | None, final_match: bool = False, third_place: bool = False):
        """
        Responsible for assembling the schema and making
        calls to create items in the database.

        :params left_player: PlayerMath | None
        :params right_player: PlayerMath | None
        :params final_math: bool default False
        :params third_place: bool default False

        :returns Match()
        """
        match_create = MatchCreate(
            left_player_name=left_player.name,
            right_player_name=right_player.name,
            left_previous_match_id=left_player.match_id,
            right_previous_match_id=right_player.match_id,
            final_match=final_match,
            third_place=third_place
        )
        return match.create_tournament_matchs(self.__db, match=match_create, tournament_id=self.__tournament_id)
    

    def create_match_to_three_players(self):
        """
        Specific for creating three-player matches
        """
        first_player = self.__players[0]
        second_player = self.__players[1]
        third_player = self.__players[2]
        
        match = self.insert_match_create(left_player=first_player, right_player=second_player)
        
        winner_match = PlayerMath(match.winner, match.id)
        self.insert_match_create(left_player=third_player, right_player=winner_match, final_match=True)

        loser_match = PlayerMath(match.loser, match.id)
        self.insert_match_create(left_player=loser_match, right_player=PlayerMath(), third_place=True)
        

    def create_finals_match(self):
        """
        Auxiliary function for creating final matches
        (final dispute and dispute for third place)
        """
        left_player = self.__players[0]
        right_player = self.__players[1]
        self.insert_match_create(left_player=left_player, right_player=right_player, final_match=True)
        self.insert_match_create(left_player=left_player, right_player=right_player, third_place=True)

    def fill_participant_vacancies(self):
        """
        To have balance between the brackets, an auxiliary
        function that completes the number of Players up to
        the next base number 2. These participants are null.
        """
        next_higher_power_of_two = int(math.pow(2, math.ceil(math.log2(len(self.__players)))))
        empty_extra_matchs = next_higher_power_of_two - len(self.__players)
        self.__players.extend([PlayerMath()] * empty_extra_matchs)

    def create_all_matchs(self):
        """
        Auxiliar function for creating matches
        """
        self.fill_participant_vacancies()
        while(len(self.__players) > 1):
            if len(self.__players) == 2:
                self.create_finals_match()
                self.__players = []
            else:
                half_length: int = int(len(self.__players)/2)
                left: list[PlayerMath | None] = self.__players[0:half_length]
                right: list[PlayerMath | None] = self.__players[half_length:]

                next_round: list[PlayerMath | None] = []
                for participant_pair in zip(left, right):
                    left_player = participant_pair[0]
                    right_player = participant_pair[1]
                    if(left_player.skippable_player()):
                        next_round.append(right_player)
                    elif(right_player.skippable_player()):
                        next_round.append(left_player)
                    else:
                        match = self.insert_match_create(left_player=left_player, right_player=right_player)
                        next_round.append(PlayerMath(match.winner, match.id))
                
                self.__players = next_round
