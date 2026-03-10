from typing import TypedDict, NotRequired
from src.RunandBunMachine.pokemon import BasePokemon, UserPokemon, BattlingPokemon

class TeamDict(TypedDict):
    slot1: NotRequired[BattlingPokemon]
    slot2: NotRequired[BattlingPokemon]
    slot3: NotRequired[BattlingPokemon]
    slot4: NotRequired[BattlingPokemon]
    slot5: NotRequired[BattlingPokemon]
    slot6: NotRequired[BattlingPokemon]


