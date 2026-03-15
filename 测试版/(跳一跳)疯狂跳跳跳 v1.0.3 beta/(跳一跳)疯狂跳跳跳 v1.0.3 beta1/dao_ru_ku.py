import importlib as ipl
import subprocess as sp
import time as tm
import sys
def DaoRuKu(needPackages):
    input("运行这个程序需要一些库，我将将会检查这些库是否已安装，按enter键开始检查")
    while True:
        missPackages=[]
        for pck,alias in needPackages.items():
            try:
                globals()[alias]=ipl.import_module(pck)
                print(f"\033[32m✓\033[0m [{pck}]库已安装")
            except ImportError:
                missPackages.append(pck)
                print(f"\033[31m✗\033[0m [{pck}]库未安装")
            tm.sleep(0.5)
        if missPackages:
            input("发现未安装的库，按下enter键开始自动安装")
            missPackages2=[]
            for pck in missPackages:
                try:
                    sp.check_call([sys.executable,"-m","pip","install",pck])
                    print(f"\033[32m✓\033[0m [{pck}]库安装成功")
                except sp.CalledProcessError:
                    missPackages2.append(pck)
                    print(f"\033[31m✗\033[0m [{pck}]库安装失败")
                tm.sleep(0.5)
            if missPackages2:
                print("\033[31m✗\033[0m 部分库安装失败，请尝试在终端手动安装缺少的包")
                print("手动安装命令：")
                for pck in missPackages2:
                    print(f"pip install {pck}")
                    tm.sleep(0.5)
                input("在终端安装完毕后，请按enter再次检测")
                continue
        break
    print("\033[32m✓\033[0m 所有库都已安装完毕")
    for pck,alias in needPackages.items():
        globals()[alias]=ipl.import_module(pck)