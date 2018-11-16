import os 

if __name__ == '__main__':
    stream = ''
    l = [i for i in os.listdir() if os.path.isdir(i)]
    for i in l:
        print(i)
        stream += '['+i+']\n'
        count = 0
        tmp = [j for j in os.listdir(i) if os.path.isfile(i+'/'+j)]
        for j in tmp:
            print(j)
            stream += str(count) +' = ' + j + '\n'
            count += 1
    
    with open('example.ini', 'w') as configfile:
        configfile.write(stream)
