from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))

from util.base import DungeonMaster

dm = DungeonMaster()

dm.start_server()