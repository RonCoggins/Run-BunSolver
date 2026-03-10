
import logging

import src.RunandBunMachine.battle_engine as be
import gui.gui




logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)



def main():
    battle = be.BattleEngine()
    gui.gui.GUI(battle)
    #test = tui.TUI()
    #test.run()

main()

    
 
 