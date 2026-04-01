from daoRuKu import DaoRuKu
#################################检查库#################################
needPackages={
    "pygame":"pg"
}
DaoRuKu(needPackages)
input("按下Enter键开始游玩")
print("游戏开始，请进入弹出的窗口")
from game import Game
game=Game()
game.run()