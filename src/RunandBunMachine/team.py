
import src.constants.opponenttrainers as opptrainers
import src.util.typed_dicts as td

import src.constants.constants as constants

import src.RunandBunMachine.pokemon as p
import src.RunandBunMachine.game_state as gs
import src.util.showdown_parser as showdown_parser
import src.ai.switchinai as siAI

class BattlingTeam:

    def __init__(self, game_state: gs.GameState, player: bool, opponent_name:str|None = None):

        self.player: bool = player
        self.game_state = game_state

        if player:
            self.opponent_name = None
        else:
            self.opponent_name = opponent_name

        self.team : td.TeamDict = {}

        self.generate_team()

        
        self.active_pokemon:p.BattlingPokemon = self.team["slot1"]
        self.remaining_pokemon: td.TeamDict = self.team.copy()
        self.fainted_pokemon: td.TeamDict = {}

        self.switch_required: bool = False

    def generate_team(self):
        
        if self.player:
            self.load_player_team()
        else:
            self.load_opponent_team()

    def load_player_team(self):
        
        trainer_team = showdown_parser.ShowdownParser().team

        pokemon_names: list[str] = list(trainer_team.keys())
        number_of_pokemon:int = len(trainer_team.keys())

        max_team_size: int = constants.MAX_TEAM_SIZE

        min_of_pokemon_and_team_size = min(number_of_pokemon,max_team_size)

        for slot_index in range(min_of_pokemon_and_team_size):

            pokemon_name = pokemon_names[slot_index]
            slot_number = f"slot{slot_index+1}"

            user_pokemon_obj = p.UserPokemon(pokemon_name=pokemon_name,
                                                   level=trainer_team[pokemon_name]["level"],
                                                   nature=trainer_team[pokemon_name]["nature"],
                                                   ability=trainer_team[pokemon_name]["ability"],
                                                   moveset=trainer_team[pokemon_name]["moves"],
                                                   ivs=trainer_team[pokemon_name]["ivs"],
                                                   )

            self.team[slot_number] = p.BattlingPokemon(user_pokemon_obj)

    def load_opponent_team(self) -> None:
        
        trainer_team: opptrainers.Trainer = opptrainers.opponent_trainers[self.opponent_name]

        pokemon_names: list[str] = list(trainer_team.keys())
        number_of_pokemon:int = len(trainer_team.keys())

        for slot_index in range(number_of_pokemon):

            pokemon_name = pokemon_names[slot_index]
            slot_number = f"slot{slot_index+1}"
            
            user_pokemon_obj = p.UserPokemon(pokemon_name=pokemon_name,
                                             level=trainer_team[pokemon_name]["level"],
                                             nature=trainer_team[pokemon_name]["nature"],
                                             ability=trainer_team[pokemon_name]["ability"],
                                             moveset=trainer_team[pokemon_name]["moves"],
                                             #ivs=trainer_team[pokemon_name]["ivs"],
                                             item=trainer_team[pokemon_name]["item"])
                                            
                                                

            self.team[slot_number] = p.BattlingPokemon(user_pokemon_obj)
                                            
    def get_team_size(self) -> int:
        return len(self.team.keys())
    
    def update_active_pokemon(self, slot_number: str):
        self.active_pokemon:p.BattlingPokemon = self.team[f"{slot_number}"]

    def update_fainted_pokemon(self) -> None:

        dict_to_be_updated:bool = False
        slot_number_of_fainted: str = ""
        fainted_pokemon: p.BattlingPokemon


        for slot_number, pokemon in self.remaining_pokemon.items():
            #print("Performing Faint Check")
            if pokemon.is_fainted == True:
                dict_to_be_updated = True
                slot_number_of_fainted = slot_number
                fainted_pokemon = pokemon

                
                print(f"{pokemon} was found to be fainted, setting flag to update dict to True")
                break
            #else:
                #print("No pokemon found to be fainted")

        if dict_to_be_updated:
            print("Adding pokemon to fainted dict")
            self.fainted_pokemon[slot_number_of_fainted] = fainted_pokemon
            self.update_remaining_pokemon(slot_number_of_fainted)
            self.switch_required = True
            if self.number_of_remaining_pokemon() > 0:
                self.perform_switch()
        
        print(f"Active Pokemon - {self.active_pokemon}")
        print(f"Remaining Pokemon - {self.remaining_pokemon}")
        print(f"Fainted Pokemon - {self.fainted_pokemon}")       
    
    def update_remaining_pokemon(self, removed_pokemon_slot:str):
          print("Updating remaining pokemon")
          self.remaining_pokemon.pop(removed_pokemon_slot)

    def perform_switch(self):
        print("Performing switch")
        if self.player:
            slot_being_switched_to: str = siAI.SwitchInAI(self.game_state,True).get_switch_in_decision()
            self.active_pokemon = self.team[slot_being_switched_to]
            print(f"Player active pokemon is now: {self.active_pokemon}")
        else:
            slot_being_switched_to: str = siAI.SwitchInAI(self.game_state,False).get_switch_in_decision()
            self.active_pokemon = self.team[slot_being_switched_to]
            print(f"Opponent active pokemon is now: {self.active_pokemon}")
    
    def number_of_remaining_pokemon(self) -> int:
        
        remaining_pokemon:list[str] = [x for x in self.remaining_pokemon.keys()]

        number_remaining: int = len(remaining_pokemon)

        return number_remaining

    def reset_team(self):
        self.team : td.TeamDict = {}
        self.generate_team()
        self.active_pokemon:p.BattlingPokemon = self.team["slot1"]
        self.remaining_pokemon: td.TeamDict = self.team.copy()
        self.fainted_pokemon: td.TeamDict = {}
        
        for pokemon in self.team.values():
            pokemon.reset_pokemon()
