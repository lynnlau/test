import os 
import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    l = [i for i in os.listdir() if os.path.isdir(i)]
    for i in l:
        count = 0
        tmp = [j for j in os.listdir(i) if os.path.isfile(i+'/'+j)]
        for j in tmp:
            config[i][str(count)] = j
            count += 1
    
    with open('example.ini', 'w') as configfile:
        config.write(configfile)
