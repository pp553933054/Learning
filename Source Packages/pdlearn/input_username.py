import sys
import time
import msvcrt


def read_input(timeout=5):
    '''
    是否需要用户标识
    :param timeout: 超时
    :type timeout: 秒
    :return: 用户标识，默认值空
    :rtype: str
    '''
    start_time = time.time()
    sys.stdout.write('是否输入用户标识（y 或者 n,默认值为：n）剩余确定时间%s秒:\n' % timeout)
    input_str = ''
    while True:
        if msvcrt.kbhit():
            char = msvcrt.getche()
            if ord(char) == 13:  # enter_key
                break
            elif ord(char) >= 32:  # space_char
                input_str += str(char, encoding='utf8')
        if (time.time() - start_time) > timeout:
            break
    username = ''
    if len(input_str) != 0 and (input_str[0] == 'y' or input_str[0] == 'Y'):
        print('\n请输入用户标识：')
        temp=input('\n')
        if len(temp)!=0:
            return temp
        # line = sys.stdin.readline()
        line=input()
        return line
    return username
