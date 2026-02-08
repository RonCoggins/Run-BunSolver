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
        height: int = 600
        width: int = 600
        root.geometry(f"{height}x{width}")

        main_frame = tk.Frame(root)
        main_frame.grid()

        self.player_team_frame = tk.Frame(
            main_frame, highlightthickness=1, highlightbackground="Black"
        )

        self.opponent_team_frame = tk.Frame(
            main_frame, highlightthickness=1, highlightbackground="Black"
        )

        player_team_frame_column = 0
        opponent_team_frame_column = 1

        self.player_team_frame.grid(row=0, column=player_team_frame_column, padx=50)
        self.opponent_team_frame.grid(row=0, column=opponent_team_frame_column, padx=50)

        

        self.create_player_pokemon_team()
        self.create_available_trainers_list(self.opponent_team_frame)
        
        


        stats_display_frame = tk.Frame(
            main_frame, highlightthickness=1, highlightbackground="Black"
        )
        stats_display_frame.grid(row=1, column=0, padx=50)

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

    def create_available_trainers_list(self,parent_frame: tk.Frame):
        available_trainers = list(opponenttrainers.opponent_trainers.keys())
        self.trainers_combobox = ttk.Combobox(parent_frame, values=available_trainers)
        self.trainers_combobox.set("Select Opponent Trainer")
        self.trainers_combobox.grid(column=1,row=0)
        self.trainers_combobox.bind("<<ComboboxSelected>>", self.create_trainer_team)
    
    @cache
    def create_trainer_team(self, event):
        
        trainer_selection = self.trainers_combobox.get()
        trainer_team = t.BattlingTeam(False, trainer_selection)
        

        self.opponent_pokemon_image0 = tk.Label(self.opponent_team_frame)
        self.opponent_pokemon_image1 = tk.Label(self.opponent_team_frame)
        self.opponent_pokemon_image2 = tk.Label(self.opponent_team_frame)
        self.opponent_pokemon_image3 = tk.Label(self.opponent_team_frame)
        self.opponent_pokemon_image4 = tk.Label(self.opponent_team_frame)
        self.opponent_pokemon_image5 = tk.Label(self.opponent_team_frame)
        self.opponent_pokemon_image0.grid(column=0,row=2)
        self.opponent_pokemon_image1.grid(column=1,row=2)
        self.opponent_pokemon_image2.grid(column=2,row=2)
        self.opponent_pokemon_image3.grid(column=0,row=3)
        self.opponent_pokemon_image4.grid(column=1,row=3)
        self.opponent_pokemon_image5.grid(column=2,row=3)
        self.load_opponent_pokemon_png(trainer_team)
    
    @cache
    def load_opponent_pokemon_png(self, team: t.BattlingTeam):
        opponent_team_pokemon_obj:list[p.BattlingPokemon] = list(team.team.values())
        opponent_team_names: list[str] = [x.pokemon_name.upper() for x in opponent_team_pokemon_obj]
    
        self.image_location0 = f"{PNG_DIRECTORY}/{opponent_team_names[0]}.png"
        self.image0 = tk.PhotoImage(file=self.image_location0,width=64)
        self.opponent_pokemon_image0['image'] = self.image0

        self.image_location1 = f"{PNG_DIRECTORY}/{opponent_team_names[1]}.png"
        self.image1 = tk.PhotoImage(file=self.image_location1,width=64)
        self.opponent_pokemon_image1['image'] = self.image1

        self.image_location2 = f"{PNG_DIRECTORY}/{opponent_team_names[2]}.png"
        self.image2 = tk.PhotoImage(file=self.image_location2,width=64)
        self.opponent_pokemon_image2['image'] = self.image2

        self.image_location3 = f"{PNG_DIRECTORY}/{opponent_team_names[3]}.png"
        self.image3 = tk.PhotoImage(file=self.image_location3,width=64)
        self.opponent_pokemon_image3['image'] = self.image3

        self.image_location4 = f"{PNG_DIRECTORY}/{opponent_team_names[4]}.png"
        self.image4 = tk.PhotoImage(file=self.image_location4,width=64)
        self.opponent_pokemon_image4['image'] = self.image4

        self.image_location5 = f"{PNG_DIRECTORY}/{opponent_team_names[5]}.png"
        self.image5 = tk.PhotoImage(file=self.image_location5,width=64)
        self.opponent_pokemon_image5['image'] = self.image5
    
    def create_player_pokemon_team(self):

        player_team_label = tk.Label(self.player_team_frame, text="Player Team")
        player_team_label.grid(column=1,row=0)

        self.player_pokemon_image0 = tk.Label(self.player_team_frame)
        self.player_pokemon_image1 = tk.Label(self.player_team_frame)
        self.player_pokemon_image2 = tk.Label(self.player_team_frame)
        self.player_pokemon_image3 = tk.Label(self.player_team_frame)
        self.player_pokemon_image4 = tk.Label(self.player_team_frame)
        self.player_pokemon_image5 = tk.Label(self.player_team_frame)
        self.player_pokemon_image0.grid(column=0,row=2)
        self.player_pokemon_image1.grid(column=1,row=2)
        self.player_pokemon_image2.grid(column=2,row=2)
        self.player_pokemon_image3.grid(column=0,row=3)
        self.player_pokemon_image4.grid(column=1,row=3)
        self.player_pokemon_image5.grid(column=2,row=3)
        self.load_player_pokemon_png()

    def load_player_pokemon_png(self):
        player_team_pokemon_obj:list[p.BattlingPokemon] = list(self.battle_engine.game_state.player_info.team.team.values())
        player_team_names: list[str] = [x.pokemon_name.upper() for x in player_team_pokemon_obj]
    
        self.image_location0 = f"{PNG_DIRECTORY}/{player_team_names[0]}.png"
        self.image0 = tk.PhotoImage(file=self.image_location0,width=64)
        self.player_pokemon_image0['image'] = self.image0

        self.image_location1 = f"{PNG_DIRECTORY}/{player_team_names[1]}.png"
        self.image1 = tk.PhotoImage(file=self.image_location1,width=64)
        self.player_pokemon_image1['image'] = self.image1

        self.image_location2 = f"{PNG_DIRECTORY}/{player_team_names[2]}.png"
        self.image2 = tk.PhotoImage(file=self.image_location2,width=64)
        self.player_pokemon_image2['image'] = self.image2

        self.image_location3 = f"{PNG_DIRECTORY}/{player_team_names[3]}.png"
        self.image3 = tk.PhotoImage(file=self.image_location3,width=64)
        self.player_pokemon_image3['image'] = self.image3

        self.image_location4 = f"{PNG_DIRECTORY}/{player_team_names[4]}.png"
        self.image4 = tk.PhotoImage(file=self.image_location4,width=64)
        self.player_pokemon_image4['image'] = self.image4

        self.image_location5 = f"{PNG_DIRECTORY}/{player_team_names[5]}.png"
        self.image5 = tk.PhotoImage(file=self.image_location5,width=64)
        self.player_pokemon_image5['image'] = self.image5

    


    
