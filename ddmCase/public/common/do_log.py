import time
import os


def logOutput(level,message):
    grandParent_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    logdir = grandParent_path+ '/log/log.txt'
    print(logdir)
    with open(logdir,"a+") as textfile:
    #textfile = open(Global.Path + '/log.txt',"a")
        currentTime = time.strftime('%Y-%m-%d %H:%M:%S')
        if(level.upper() == "INFO"):
            print("[%s][INFO][%s]"%(currentTime,message))
            textfile.write("[%s][INFO][%s]\n"%(currentTime,message))
        elif(level.upper() == "WARN"):
            print("[%s][WARN][%s]"%(currentTime, message))
            textfile.write("[%s][WARN][%s]\n" % (currentTime, message))
        elif (level.upper() == "ERROR"):
            print("[%s][ERROR][%s]"%(currentTime, message))
            textfile.write("[%s][ERROR][%s]\n" % (currentTime, message))
        else:
            print('log level set error!')
            textfile.write('log level set error!\n')



if __name__ == '__main__':
    logOutput('error',message='asfadsfa')