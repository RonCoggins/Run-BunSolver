import tkinter as tk
from tkinter import ttk
from pathlib import Path


import battle_engine as be


from gui.opponentteamselect import OpponentTeamSelectFrame
from gui.playerteamselect import PlayerTeamSelectFrame
from gui.battlewindow import BattleFrame



PNG_DIRECTORY = Path('./png')

class GUI:
    def __init__(self, battle_engine: be.BattleEngine):

        self.battle_engine = battle_engine
        self.battle_engine.init_game_state("Lass Tiana")

        root = tk.Tk()
        height: int = 1500
        width: int = 1000
        root.geometry(f"{height}x{width}")
        root.resizable(True,True)
        root.attributes('-fullscreen')

        main_frame = tk.Frame(root)
        main_frame.grid()

        self.opponent_team_select_frame = OpponentTeamSelectFrame(main_frame, self.battle_engine)
        self.player_team_select_frame = PlayerTeamSelectFrame(main_frame, self.battle_engine)
        self.battle_frame = BattleFrame(main_frame, self.battle_engine)
        
        self.opponent_team_select_frame.grid(row=0, column=0)
        self.player_team_select_frame.grid(row=0,column=1)
        self.battle_frame.grid(row=2)

        root.mainloop()
    




    








            
        
        

    
