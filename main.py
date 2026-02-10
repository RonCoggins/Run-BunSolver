
import logging
from timeit_decorator import timeit_sync

import battle_engine as be
import gui


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def main():
    battle = be.BattleEngine()
    gui.GUI(battle)

    
test


main()

