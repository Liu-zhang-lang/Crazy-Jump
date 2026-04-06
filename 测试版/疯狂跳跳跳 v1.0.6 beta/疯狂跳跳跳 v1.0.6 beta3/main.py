from daoRuKu import DaoRuKu
#################################检查库#################################
needPackages={
    "pygame":"pg"
}
print("---------------------------------------------------")
DaoRuKu(needPackages)
print("检查完毕！")
print("游戏开始，请进入弹出的窗口")
print("---------------------------------------------------")
from game import Game
game=Game()
game.run()