
import math
import move as m


import constants

class BasePokemon:

    def __init__(self, pokemon_name: str):

        self.pokemon_name: str = pokemon_name.lower()

        self.basestats: dict[str,int] = {
            "hp": constants.POKEMON_STATS[self.pokemon_name.lower()]["hp"],
            "atk": constants.POKEMON_STATS[self.pokemon_name.lower()]["atk"],
            "def": constants.POKEMON_STATS[self.pokemon_name.lower()]["def"],
            "spa": constants.POKEMON_STATS[self.pokemon_name.lower()]["spa"],
            "spd": constants.POKEMON_STATS[self.pokemon_name.lower()]["spd"],
            "spe": constants.POKEMON_STATS[self.pokemon_name.lower()]["spe"],
        }

        self.typing = {
            "type1": constants.POKEMON_STATS[self.pokemon_name.lower()]["type1"],
            "type2": constants.POKEMON_STATS[self.pokemon_name.lower()]["type2"],
        }

class UserPokemon(BasePokemon):
    def __init__(
        self,
        pokemon_name: str,
        level: int,
        nature: str,
        ability: str,
        moveset: list[str],
        ivs: tuple[int, int, int, int, int, int] = (31, 31, 31, 31, 31, 31),
        item: str|None = None,
    ):

        self.base_pokemon = BasePokemon(pokemon_name)
        self.level = level
        self.nature = nature
        self.ability = ability
        self.item = item
        print(ivs)
        self.ivs: dict[str, int] = {
            "hp": ivs[0],
            "atk": ivs[1],
            "def": ivs[2],
            "spa": ivs[3],
            "spd": ivs[4],
            "spe": ivs[5],
        }

        self.moveset = {
            "move1": m.Move(moveset[0]),
            "move2": m.Move(moveset[1]),
            "move3": m.Move(moveset[2]),
            "move4": m.Move(moveset[3]),
        }

        # Calculated Info

        self.stats: dict[str, int] = {
            "hp": self.calculate_stats("hp"),
            "atk": self.calculate_stats("atk"),
            "def": self.calculate_stats("def"),
            "spa": self.calculate_stats("spa"),
            "spd": self.calculate_stats("spd"),
            "spe": self.calculate_stats("spe"),
        }

    def calculate_stats(self, stat:str) -> int:
        if stat != "hp":
            ev_calc: int = int(1 / 4)  # Placeholder for EVs

            calculation:int = 2 * self.base_pokemon.basestats[stat] + self.ivs[stat] + ev_calc
            calculation *= self.level
            calculation = math.floor(calculation / 100)
            calculation += 5
            calculation = math.floor(calculation * 1)

            return calculation
        else:

            ev_calc:int = int(1 / 1)  # Placeholder for EVs

            calculation:int = int(
                ((2 * self.base_pokemon.basestats["hp"] + self.ivs["hp"])) * self.level / 100
            )

            calculation += (self.level + 10)

            return calculation

class BattlingPokemon(UserPokemon):
    def __init__(self, pokemon: UserPokemon):
        
        self.UserPokemon = pokemon
        self.pokemon_name = pokemon.base_pokemon.pokemon_name
        self.typing = pokemon.base_pokemon.typing
        self.moveset = pokemon.moveset
        self.level = pokemon.level
        self.ability = pokemon.ability
        self.stats = pokemon.stats
        

        self.current_HP: int = self.UserPokemon.stats["hp"]

        self.is_fainted: bool = False

    def __repr__(self):
        return self.pokemon_name
    
    def reduce_HP(self, value:int):
        self.current_HP -= value

        if self.current_HP < 0:
            self.current_HP = 0
            self.is_fainted = True
            print(f"{self.pokemon_name} has Fainted")
        
        print(f"{self.pokemon_name}'s HP was reduced by {value}\n HP is now {self.current_HP}")
    
    def reset_pokemon(self):
        self.current_HP: int = self.UserPokemon.stats["hp"]
        self.is_fainted: bool = False
            