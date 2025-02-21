from dataclasses import dataclass

@dataclass
class GameConfig:
    '''Class for game configuration'''
    width: int
    height: int
    caption: str
    fps: int = 60
    bg_color :tuple[int, int, int] = (90, 90, 90)

