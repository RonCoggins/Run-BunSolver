import tkinter as tk
from tkinter import ttk
from pathlib import Path
from functools import cache

import numpy as np

import src.RunandBunMachine.team as t
import src.RunandBunMachine.pokemon as p
import src.RunandBunMachine.game_state as gs
import src.RunandBunMachine.battle_engine as be

from gui.util import BlankFrame


class PokemonInformationFrame(tk.Frame):
    def __init__(self, parent_frame: tk.Frame, battling_pokemon_obj: p.BattlingPokemon):
        tk.Frame.__init__(self, parent_frame)
        self.battling_pokemon_obj = battling_pokemon_obj
        
        self.parent_frame = parent_frame

        self.pokemon_name = tk.Label(self, text=f"{self.get_name()}")
        self.level = tk.Label(self, text=f"Lvl: {self.get_level()}")
        self.hp = tk.Label(self, text=f"HP: {self.get_HP()}")
        self.moveset = tk.Label(self, text=self.get_moveset())

        self.stat_mapping: dict[str,int] = {
            "name": 0,
            "lvl" : 1,
            "hp" : 2,
            "moveset" : 3,
        }

        self.pokemon_name.grid(row=self.stat_mapping["name"])
        self.level.grid(row=self.stat_mapping["lvl"])
        self.hp.grid(row=self.stat_mapping["hp"])
        self.moveset.grid(row=self.stat_mapping["moveset"])

    
    def get_name(self) -> str:

        return self.battling_pokemon_obj.pokemon_name.title()

    def get_level(self) -> int:

        return self.battling_pokemon_obj.level

    def get_HP(self) -> int:

        return self.battling_pokemon_obj.current_HP
    
    def get_moveset(self) -> list:

        moveset = list(self.battling_pokemon_obj.moveset.values())
        moveset = [x.move_name.title() for x in moveset]

        formatted_string = ""

        for movename in moveset:
           formatted_string = formatted_string + movename +"\n"
        
        return formatted_string