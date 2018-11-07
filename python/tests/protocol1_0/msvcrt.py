import msvcrt  #測試msvcrt
  #  print("press escape to quit")

while 1:
    char = msvcrt.getch()
    if char == chr(27):  # 当输入esc则退出
        exit()
    print(char)
    if char == chr(13):
        print(char)