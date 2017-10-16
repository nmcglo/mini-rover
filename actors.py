from enum import Enum, auto


class Color(Enum):
    RED = 0
    GREEN = auto()
    BLUE = auto()
    MAGENTA = auto()
    CYAN = auto()
    YELLOW = auto()

    colorMap = {self.RED:[1,0,0], self.GREEN:[0,1,0], self.BLUE:[0,0,1], self.MAGENTA:[1,0,1],self.CYAN:[0,1,1], self.YELLOW:[1,1,0]}

    def getRGB(self):
        return self.colorMap[self]


class Mood(Enum):
    NORMAL = 0
    ALERT = auto()
    ERROR = auto()
    STANDBY = auto()
    SCANNING = auto()



class MoodLED(Mood):

   def getRGB(self):




class MoodIndicator:

    def __init__(self):
        self.mood = Mood.NORMAL

    def 