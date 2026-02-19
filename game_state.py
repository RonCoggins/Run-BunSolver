

from typing import Any
import move as m
import pokemon as p
import team as t

class GameState():

    def __init__(self, opponent_trainer:str = "Youngster Tommy"):
        
        self.opponent_info = GameStateOpponentInfo(opponent_trainer= opponent_trainer)
        self.player_info = GameStatePlayerInfo()
        self.turn_info = GameStateTurnInfo()

        self.battle_over: bool = False
        self.winner: str = ""

    def determine_if_winner(self):

        if self.opponent_info.team.number_of_remaining_pokemon() == 0:
            self.winner = "player"
            self.battle_over = True
            return True
        if self.player_info.team.number_of_remaining_pokemon() == 0:
            self.winner = "opponent"
            self.battle_over = True
            return True
        return False
    
    def reset_state(self):
        self.battle_over: bool = False
        self.winner: str = ""
        self.opponent_info.team.reset_team()
        self.player_info.team.reset_team()
        self.turn_info.reset_state()

class GameStateOpponentInfo():

    def __init__(self, opponent_trainer:str = "Youngster Tommy"):

        self.trainer: str = opponent_trainer
        self.team: t.BattlingTeam = t.BattlingTeam(player=False, opponent_name=self.trainer)
        self.no_of_pokemon: int = self.team.get_team_size()
        self.current_move: m.Move = ""
        

    def reset_state(self):
        self.team.reset_team()

class GameStatePlayerInfo():

    def __init__(self):

        self.team: t.BattlingTeam = t.BattlingTeam(player=True)
        self.no_of_pokemon: int = self.team.get_team_size()
        self.current_move: m.Move = ""
        
    
    def reset_state(self):
        self.team.reset_team()

class GameStateTurnInfo():

    def __init__(self):

        
        self.turn_number: int = 1

        self.first_mover: str

    def reset_state(self):
        self.turn_number = 1



        
        

        
        

        
       

        
        

        
        

        
        

        

    #     self.turn_number = 1

    #     # Branching Path Modifiers

    #     self.player_critical_hit: bool = False
    #     self.opponent_critical_hit: bool = False

    #     # Tree Indentification

    #     self.current_node_identifier: str = self.set_turn_0_node_ID()
    #     self.previous_node_identifier: str

    # def reduce_pokemon_hp(self, user: str, damage: int) -> None:
    #     if user == "player_pokemon":
    #         self.active_player_pokemon_currentHP = max(
    #             self.active_player_pokemon_currentHP - damage, 0
    #         )
    #     if user == "opponent_pokemon":
    #         self.active_opponent_pokemon_currentHP = max(
    #             self.active_opponent_pokemon_currentHP - damage, 0
    #         )

    # def switch_player_pokemon(self, slot_number: str):
    #     self.active_player_pokemon = self.player_team.player_team[slot_number]
    #     self.active_player_pokemon_currentHP: int = self.player_team.player_team[
    #         slot_number
    #     ].stats["hp"]
    #     self.player_team_pokemon_remaining: int = self.no_of_player_pokemon - len(
    #         self.player_fainted_pokemon
    #     )
    #     self.active_player_pokemon_slot = slot_number
    #     self.player_critical_hit: bool = False

    # def switch_opponent_pokemon(self, slot_number: str):
    #     self.active_opponent_pokemon = self.opponent_team.opponent_team[slot_number]
    #     self.active_opponent_pokemon_currentHP: int = self.opponent_team.opponent_team[
    #         slot_number
    #     ].stats["hp"]
    #     self.opponent_team_pokemon_remaining: int = self.no_of_opponent_pokemon - len(
    #         self.opponent_fainted_pokemon
    #     )
    #     self.active_opponent_pokemon_slot = slot_number
    #     self.opponent_critical_hit: bool = False

    # def determine_combinations(self):

    #     critical_hit_combinations: tuple[tuple[bool]] = ((True,False),
    #                                                     (player=True,opponent=True),
    #                                                     (player=False,opponent=True),
    #                                                     (player=False,opponent=False))

    #     return critical_hit_combinations




    # def update_node_ID(self) -> None:
    #     self.update_previous_node_ID()
    #     self.update_current_node_ID()

    # def update_previous_node_ID(self) -> None:
    #     self.previous_node_identifier = self.current_node_identifier

    # def update_current_node_ID(self) -> None:
    #     self.current_node_identifier = str(
    #         f"TN:{self.turn_number} PMove:{self.current_player_move.move_name} PCriticalHit: {self.player_critical_hit} OMove:{self.current_opponent_move.move_name} OCriticalHit: {self.opponent_critical_hit}"
    #     )

    # def set_turn_0_node_ID(self) -> str:
    #     return str(f"root")
