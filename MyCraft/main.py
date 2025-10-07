from direct.showbase.ShowBase import ShowBase
from mapmanager import Mapmanager
from hero import Hero

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land = Mapmanager()
        x,y = self.land.loadLand('Lands/land.txt')
        self.hero = Hero((11, 11, 3), self.land)
        base.camLens.setFov(120)


game = Game()
game.run()