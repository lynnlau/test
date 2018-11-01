import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('请选择测试脚本')
    else:
        with open('./CommadTask','w') as file:
            i = 1
            while sys.argv[i:]:
                file.write(sys.argv[i]+'\n')
                i += 1
            file.close()
    
    
    
    
