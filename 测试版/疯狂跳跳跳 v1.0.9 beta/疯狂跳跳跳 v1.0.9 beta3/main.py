from checkLib import check_lib
#################################检查库#################################
needPackages={
    "pygame",
    "pyperclip"
}
print("---------------------------------------------------")
check_lib(needPackages)
print("检查完毕！")
print("游戏开始，请进入弹出的窗口")
print("---------------------------------------------------")
from game import Game
game=Game()
game.run()