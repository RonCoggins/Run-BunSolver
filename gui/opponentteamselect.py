import src.RunandBunMachine.battle_engine as battle_engine
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from functools import cache

import numpy as np

import src.RunandBunMachine.team as t
import src.RunandBunMachine.pokemon as p
import src.RunandBunMachine.game_state as gs
import src.RunandBunMachine.battle_engine as be
import src.constants.opponenttrainers as opponenttrainers

from gui.pokemoninfoframe import PokemonInformationFrame
from gui.util import BlankFrame

PNG_DIRECTORY = Path('./gui/assets/png')

class OpponentTeamSelectFrame(tk.Frame):

    def __init__(self, parent_frame: tk.Frame, battle_engine: be.BattleEngine):
        tk.Frame.__init__(self, parent_frame)

        self.config(highlightbackground="black",highlightthickness=1, padx=10)
        self.config(height=250, width=600)
        self.grid_propagate(False)
        self.grid_propagate(False)

        self.parent_frame = parent_frame
        self.battle_engine = battle_engine

        self.first_load:bool  = True

        self.opponent_team_info_dict: dict[str,tk.Label] = {}
        self.stat_frame_dict: dict[str,tk.Frame] = {}

        self.create_available_trainers_list()

    def create_available_trainers_list(self):
        available_trainers: list[str] = list(opponenttrainers.opponent_trainers.keys())
        self.trainers_combobox = ttk.Combobox(self, values=available_trainers)
        self.trainers_combobox.set("Select Opponent Trainer")
        self.trainers_combobox.grid(column=1,row=0)
        self.trainers_combobox.bind("<<ComboboxSelected>>", self.display_team_info)

    def display_team_info(self, event):

        trainer_selection: str = self.trainers_combobox.get()
        self.battle_engine.init_game_state(trainer_selection)
        trainer_team = t.BattlingTeam(self.battle_engine.game_state,False, trainer_selection)
        opponent_team_pokemon_obj:list[p.BattlingPokemon] = list(trainer_team.team.values())
        self.opponent_team_names: list[str] = [x.pokemon_name.upper() for x in opponent_team_pokemon_obj]

        column = 0
        row = 2

        self.destroy_existing_frames()

        for index in range(6):
            
            if index < len(self.opponent_team_names):
                
                self.opponent_team_info_dict[f"image{index}"] = tk.Label(self)

                self.stat_frame_dict[f"infoframe{index}"] = PokemonInformationFrame(self, opponent_team_pokemon_obj[index])
                self.stat_frame_dict[f"infoframe{index}"].config(height=64,width=64)

                self.opponent_team_info_dict[f"image{index}"].grid(column=column,row=row) 
                self.stat_frame_dict[f"infoframe{index}"].grid(column=column+1,row=row)
            else:
                
                self.opponent_team_info_dict[f"image{index}"] = tk.Label(self)
                self.stat_frame_dict[f"infoframe{index}"] = BlankFrame(self)
                self.opponent_team_info_dict[f"image{index}"].grid(column=column,row=row)
                self.stat_frame_dict[f"infoframe{index}"].grid(column=column+1,row=row)


            if column < 3:
                column += 2
            else:
                column = 0
                row += 1
        
        self.load_opponent_pokemon_png()

    def load_opponent_pokemon_png(self):


        self.opponent_png_locations: dict[str, str] = {}
        self.opponent_photo_image_obj: dict[str, tk.PhotoImage] = {}


        for index, pokemon_name in enumerate(self.opponent_team_names):

            self.opponent_png_locations[f"image{index}"] = f"{PNG_DIRECTORY}/{pokemon_name}.png"
            self.opponent_photo_image_obj[f"image{index}"] = tk.PhotoImage(file=self.opponent_png_locations[f"image{index}"],width=64)
            self.opponent_team_info_dict[f"image{index}"]["image"] = self.opponent_photo_image_obj[f"image{index}"]

    def destroy_existing_frames(self):

        for key in self.stat_frame_dict.keys():
            self.stat_frame_dict[key].destroy()
        for key in self.opponent_team_info_dict.keys():
            self.opponent_team_info_dict[key].destroy()

