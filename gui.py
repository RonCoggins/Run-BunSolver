import tkinter as tk
from tkinter import ttk
from pathlib import Path
from functools import cache

import team as t
import pokemon as p
import random
import game_state as gs
import battle_engine as be
import opponenttrainers

PNG_DIRECTORY = Path('./png')


class GUI:
    def __init__(self, battle_engine: be.BattleEngine):

        self.battle_engine = battle_engine

        root = tk.Tk()
        height: int = 900
        width: int = 900
        root.geometry(f"{height}x{width}")
        root.resizable(False,False)

        main_frame = tk.Frame(root)
        main_frame.grid()

        self.player_team_frame = PlayerPokemonInfoFrame(main_frame, battle_engine=self.battle_engine)
        self.opponent_team_frame = OpponentPokemonInfoFrame(main_frame, battle_engine=self.battle_engine)

        self.player_team_frame.grid(row=0, column=0)
        self.opponent_team_frame.grid(row=0, column=1)

        self.player_team_frame.rowconfigure(1)
        self.opponent_team_frame.rowconfigure(1)

        self.player_team_frame.columnconfigure(1)
        self.opponent_team_frame.columnconfigure(1)


        ### PLAYER POKEMON LIST BOX

        ### Start Battle Button
        
    #     tk.Button(battle_frame, text="Start Battle", command=lambda: [self.battle_engine.run_one_turn(), self.update_labels()]).grid(row=4)
    #     tk.Button(battle_frame, text="Simulate Full Battle", command=lambda: [self.battle_engine.finish_battle(), self.update_labels()]).grid(row=5)
    #     tk.Button(battle_frame, text="Reset Battle", command=lambda: [self.battle_engine.reset_battle(), self.update_labels()]).grid(row=6)


    #     self.turn_var = tk.StringVar()
    #     self.turn_var.set("Turn Number: " + str(self.battle_engine.game_state.turn_info.turn_number)) 
    #     tk.Label(battle_frame, textvariable=self.turn_var).grid(row=0, column=0)

    #     self.player_pokemon_var = tk.StringVar()
    #     self.player_pokemon_var.set("Player Pokemon: " + str(self.battle_engine.game_state.player_info.team.active_pokemon).title()) 
    #     tk.Label(battle_frame, textvariable=self.player_pokemon_var).grid(row=1,column=0)

    #     self.opponent_pokemon_var = tk.StringVar()
    #     self.opponent_pokemon_var.set("Opponent Pokemon: " + str(self.battle_engine.game_state.opponent_info.team.active_pokemon).title()) 
    #     tk.Label(battle_frame, textvariable=self.opponent_pokemon_var).grid(row=2,column=0)

    #     tk.Label(battle_frame, text="HP").grid(row=0, column=1)

    #     self.player_pokemon_health_var = tk.StringVar()
    #     self.player_pokemon_health_var.set(str(self.battle_engine.game_state.player_info.team.active_pokemon.current_HP)) 
    #     tk.Label(battle_frame, textvariable=self.player_pokemon_health_var).grid(row=1,column=1)

    #     self.opponent_pokemon_health_var = tk.StringVar()
    #     self.opponent_pokemon_health_var.set(str(self.battle_engine.game_state.opponent_info.team.active_pokemon.current_HP)) 
    #     tk.Label(battle_frame, textvariable=self.opponent_pokemon_health_var).grid(row=2,column=1)

    #     tk.Label(battle_frame, text="Last Move Used").grid(row=0, column=2)

    #     self.player_pokemon_move_used_var = tk.StringVar()
    #     self.player_pokemon_move_used_var.set(str(self.battle_engine.game_state.player_info.current_move)) 
    #     tk.Label(battle_frame, textvariable=self.player_pokemon_move_used_var).grid(row=1,column=2)

    #     self.opponent_pokemon_move_used_var = tk.StringVar()
    #     self.opponent_pokemon_move_used_var.set(str(self.battle_engine.game_state.opponent_info.current_move)) 
    #     tk.Label(battle_frame, textvariable=self.opponent_pokemon_move_used_var).grid(row=2,column=2)

    #     self.player_pokemon_remaining_var = tk.StringVar()
    #     self.player_pokemon_remaining_var.set(str(self.battle_engine.game_state.player_info.team.team))
    #     tk.Label(stats_display_frame, textvariable=self.player_pokemon_remaining_var,wraplength=100,justify="left").grid(row=2,column=2)
        
    #     self.available_trainers = self.create_available_trainers_list(stats_display_frame)
    #     self.available_trainers.grid(row=5, column=2)

    #     self.opponent_pokemon_remaining_var = tk.StringVar()
    #     self.opponent_pokemon_remaining_var.set(str(self.battle_engine.game_state.opponent_info.team.team))
    #     tk.Label(stats_display_frame, textvariable=self.opponent_pokemon_remaining_var,wraplength=100,justify="left").grid(row=3,column=2)

    #     image_location = f"{PNG_DIRECTORY}/ZOROARK.png"

    #     image = tk.PhotoImage(file=image_location)
    #     self.pokemon_image: tk.Label = tk.Label(stats_display_frame, image=image)
    #     self.pokemon_image.grid(column=1, row = 10)
        

        root.mainloop()
    
    # def update_labels(self) -> None:
    #     self.turn_var.set("Turn Number: " + str(self.battle_engine.game_state.turn_info.turn_number)) 

    #     self.player_pokemon_var.set("Player Pokemon: " + str(self.battle_engine.game_state.player_info.team.active_pokemon).title()) 
    #     self.opponent_pokemon_var.set("Opponent Pokemon: " + str(self.battle_engine.game_state.opponent_info.team.active_pokemon).title())

    #     self.player_pokemon_health_var.set(str(self.battle_engine.game_state.player_info.team.active_pokemon.current_HP)) 
    #     self.opponent_pokemon_health_var.set(str(self.battle_engine.game_state.opponent_info.team.active_pokemon.current_HP))

    #     self.player_pokemon_move_used_var.set(str(self.battle_engine.game_state.player_info.current_move))
    #     self.opponent_pokemon_move_used_var.set(str(self.battle_engine.game_state.opponent_info.current_move))

    #     self.player_pokemon_remaining_var.set(str(self.battle_engine.game_state.player_info.team.team))

    

    
    


    
class PlayerPokemonInfoFrame(tk.Frame):
    def __init__(self, parent_frame: tk.Frame, battle_engine: be.BattleEngine):
        tk.Frame.__init__(self, parent_frame)
   
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
            self.stat_frame_dict[f"infoframe{index}"] = PokemonStatInformationFrame(self, player_team_pokemon_obj[index])
            self.stat_frame_dict[f"infoframe{index}"].config(height=64,width=64)

            self.player_team_info_dict[f"image{index}"].grid(column=column,row=row) 
            self.stat_frame_dict[f"infoframe{index}"].grid(column=column+1,row=row)

            if column < 2:
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
    
    

class OpponentPokemonInfoFrame(tk.Frame):

    def __init__(self, parent_frame: tk.Frame, battle_engine: be.BattleEngine):
        tk.Frame.__init__(self, parent_frame)
        self.config(background="blue")
        self.parent_frame = parent_frame
        self.battle_engine = battle_engine

        

        self.create_available_trainers_list()

    def create_available_trainers_list(self):
        available_trainers = list(opponenttrainers.opponent_trainers.keys())
        self.trainers_combobox = ttk.Combobox(self, values=available_trainers)
        self.trainers_combobox.set("Select Opponent Trainer")
        self.trainers_combobox.grid(column=1,row=0)
        self.trainers_combobox.bind("<<ComboboxSelected>>", self.create_opponent_pokemon_team)

    def create_opponent_pokemon_team(self, event):

        trainer_selection = self.trainers_combobox.get()
        trainer_team = t.BattlingTeam(False, trainer_selection)

        opponent_team_pokemon_obj:list[p.BattlingPokemon] = list(trainer_team.team.values())
        self.opponent_team_names: list[str] = [x.pokemon_name.upper() for x in opponent_team_pokemon_obj]

        self.refresh_frames()
        
        self.opponent_team_info_dict: dict[str,tk.Label] = {}

        self.stat_frame_dict: dict[str,tk.Frame] = {}

        column = 0
        row = 2
        
        for index in range(len(self.opponent_team_names)):

            self.opponent_team_info_dict[f"image{index}"] = tk.Label(self)
            self.stat_frame_dict[f"infoframe{index}"] = PokemonStatInformationFrame(self, opponent_team_pokemon_obj[index])
            self.stat_frame_dict[f"infoframe{index}"].config(height=64,width=64)

            self.opponent_team_info_dict[f"image{index}"].grid(column=column,row=row) 
            self.stat_frame_dict[f"infoframe{index}"].grid(column=column+1,row=row)
            if column < 2:
                column += 1
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

    def refresh_frames(self):

        self.blank_frames: dict[str, tk.Frame] = {}

        column = 0
        row = 2

        for index in range(5):
            self.blank_frames[f"frame{index}"] = tk.Frame(self, height=64, width=64)
            self.blank_frames[f"frame{index}"].grid(column=column,row=row)

            if column < 2:
                column += 1
            else:
                column = 0
                row += 1

class PokemonStatInformationFrame(tk.Frame):
    def __init__(self, parent_frame: tk.Frame, battling_pokemon_obj: p.BattlingPokemon):
        tk.Frame.__init__(self, parent_frame)
        self.battling_pokemon_obj = battling_pokemon_obj

        self.parent_frame = parent_frame

        self.pokemon_name = tk.Label(self, text=f"Name: {self.get_name()}")
        self.level = tk.Label(self, text=f"Lvl: {self.get_level()}")

        self.stat_mapping: dict[str,int] = {
            "name": 0,
            "lvl" : 1
        }

        self.pokemon_name.grid(row=self.stat_mapping["name"])
        self.level.grid(row=self.stat_mapping["lvl"])
    
    def get_name(self) -> str:

        return self.battling_pokemon_obj.pokemon_name.title()

    def get_level(self) -> int:

        return self.battling_pokemon_obj.level


    