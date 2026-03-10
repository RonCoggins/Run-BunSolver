import tkinter as tk
from tkinter import ttk
from pathlib import Path
from functools import cache

import numpy as np

import src.RunandBunMachine.team as t
import src.RunandBunMachine.pokemon as p
import src.RunandBunMachine.game_state as gs
import src.RunandBunMachine.battle_engine as be

from gui.pokemoninfoframe import PokemonInformationFrame
from gui.util import BlankFrame

PNG_DIRECTORY = Path('./gui/assets/png')

class PlayerTeamSelectFrame(tk.Frame):
    def __init__(self, parent_frame: tk.Frame, battle_engine: be.BattleEngine):
        tk.Frame.__init__(self, parent_frame)

        self.config(highlightbackground="black",highlightthickness=1, padx=10)
        self.config(height=250, width=600)
        self.grid_propagate(False)

        self.first_load:bool  = True

        self.parent_frame = parent_frame
        self.battle_engine = battle_engine

        self.create_player_pokemon_team()


    def create_player_pokemon_team(self):

        self.player_team_label = tk.Label(self, text="Player Team")
        self.player_team_label.grid(column=1,row=0)

        player_team_pokemon_obj:list[p.BattlingPokemon] = list(self.battle_engine.game_state.player_info.team.team.values())
        self.player_team_names: list[str] = [x.pokemon_name.upper() for x in player_team_pokemon_obj]

        self.player_team_info_dict: dict[str,tk.Label] = {}
                                                          
        self.stat_frame_dict: dict[str,tk.Frame] = {}

        column = 0
        row = 2
        
        for index in range(len(self.player_team_names)):
            self.player_team_info_dict[f"image{index}"] = tk.Label(self)
            self.stat_frame_dict[f"infoframe{index}"] = PokemonInformationFrame(self, player_team_pokemon_obj[index])
            self.stat_frame_dict[f"infoframe{index}"].config(height=64,width=64)

            self.player_team_info_dict[f"image{index}"].grid(column=column,row=row) 
            self.stat_frame_dict[f"infoframe{index}"].grid(column=column+1,row=row)

            if column < 3:
                column += 2
            else:
                column = 0
                row += 1

        self.load_player_pokemon_png()

    def load_player_pokemon_png(self):
    
        self.player_png_locations: dict[str, str] = {}
        self.player_photo_image_obj: dict[str, tk.PhotoImage] = {}

        for index, pokemon_name in enumerate(self.player_team_names):

            self.player_png_locations[f"image{index}"] = f"{PNG_DIRECTORY}/{pokemon_name}.png"
            self.player_photo_image_obj[f"image{index}"] = tk.PhotoImage(file=self.player_png_locations[f"image{index}"],width=64)
            self.player_team_info_dict[f"image{index}"]["image"] = self.player_photo_image_obj[f"image{index}"]