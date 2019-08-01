'''
###get keyboard input and timeout =5

import sys, time, msvcrt

def readInput( caption, default, timeout = 5):
 start_time = time.time()
 sys.stdout.write('%s(%s):'%(caption, default));
 input = ''
 while True:
  if msvcrt.kbhit():
   char = msvcrt.getche()
   if ord(char) == 13: # enter_key
    break
   elif ord(char) >= 32: #space_char
    input += char
  if len(input) == 0 and (time.time() - start_time) > timeout:
   break

 print '' # needed to move to next line
 if len(input) > 0:
  return input
 else:
  return default

readInput("TEst1",10)

'''

import sys, time, msvcrt


def read_key_board_input(timeout=5):
    """
    默认值返回False
    :param timeout:设置超时
    :type timeout:time
    :return:True or False
    :rtype:bool
    """
    start_time = time.time()
    confirm_time = time.time()
    confirm_text = 0
    cancel_text = 0
    sys.stdout.write("是否输入用户标识（y or n ,默认值为:n）并按回车键确认");
    while True:
        if msvcrt.kbhit():
            char = msvcrt.getche()
            temp = ord(char)
            if cancel_text == 0 and (ord(char) == 121 or ord(char) == 89):  # y or Y
                confirm_text = ord(char)
                confirm_time = time.time()
                continue
            if confirm_text == 0 and (ord(char) == 110 or ord(char) == 78):  # n or N
                cancel_text = ord(char)
                start_time = time.time()
                continue
            # 输入y 或者Y 并回车
            if confirm_text != 0 and ord(char) == 13:  # enter_key
                return True
            # 直接回车
            if ord(char) == 13:
                return False
            # if ord(char) == 27:  # ESC
            #     return True
        # 输入n 或者N后未按回车超时执行
        if confirm_text == 0 and (time.time() - start_time > timeout):
            return False
        ##输入y 或者Y后未按回车超时执行
        if cancel_text == 0 and confirm_text != 0 and (time.time() - confirm_time > timeout):
            return True


if __name__ == '__main__':
    status = read_key_board_input(10)
    if status:
        text = input("请输入姓名：")
        print(text)
