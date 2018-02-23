import psutil
import subprocess
from peewee import *
from queue import Queue
import threading
import time

db = SqliteDatabase('calla.db')

STDOUT = subprocess.PIPE
STDERR = subprocess.PIPE

class Log(Model):
    name = CharField(default  ='')
    # 线程开始时间
    start_time = DateField(default = time.time())
    # 线程结束时间
    end_time = DateField(default = '')
    # 线程运行时间
    run_time = TimeField(default = 0)
    # 线程pid
    pid = IntegerField(default = -1)
    # 线程状态
    status = CharField(default = 'waiting')
    # 命令输出正文
    log = CharField(default = '')
    # 命令原文
    command = CharField(default = '')
    # 内存使用率, 用逗号分隔
    memory_percent = CharField(default  = '')
    # 内存使用， rss 实际内存， vms 虚拟内存
    memory_info = CharField(default = '')
    class Meta:
        database = db

db.connect()
db.create_tables([Log])

q = Queue()

def run(command):
    '''
    状态：status
    开始时间： start_at
    结束时间: end_at
    运行时间： 7s
    进程号： 12987
    输出： ''
    命令： command

    Args:
        command: list
        ['ping', '-c', '4', 'baidu.com']
    '''
    log = Log(
    )
    log.save()
    q.put((command, log.id))
    # q.put((p, log.id, p.pid))
    return command, id

# STDOUT = subprocess.PIPE
# STDERR = subprocess.PIPE

def log_worker():
    ''' 日志记录线程'''
    print('log worker')
    while True:
        command, id = q.get()
        proc = psutil.Popen(command, bufsize  = 0, stdout = STDOUT, stderr = STDERR)
        log = Log.select().where(Log.id == id).get()
        log.status = 'running'
        log.pid = proc.pid
        log.save()
        while True:
            memory_percent = str(proc.memory_percent())
            log.memory_percent = log.memory_percent + memory_percent + '\n'
            mem = proc.memory_info()
            memory_info = 'rss:{rss}, vms:{vms}'.format(rss = mem.rss, vms = mem.vms)
            log.memory_info = log.memory_info + memory_info + '\n'
            line = proc.stdout.readline()
            if not line:
                line = proc.stderr.readline()
            if not line:
                break
            print(line)
            line = line.decode('utf-8')
            log.log = log.log + line
            log.save()

        log.status = proc.status()
        now = time.time()
        print("结束时间：{}".format(now))
        print("程序用时：{}".format(now - log.start_time))
        # log 状态
        log.status = 'finished'
        # 结束时间
        log.end_time = now
        # 运行时间， 单位秒
        log.run_time = now - log.start_time
        log.save()

        print("Done.")
        q.task_done()


def add_task(command):
    ''' 向队列中添加 command
    返回 log id
    '''
    # command = input()
    # command = command.split(' ')
    log = Log(
        command = '\n'.join(command)
    )
    log.save()
    q.put((command, log.id))

    return log.id

def start_thread(target, args = (), daemon = False):
    t = threading.Thread(target = target, args = args)
    t.setDaemon(daemon)
    t.start()

    return t


def main():
    # t1 = threading.Thread(target = add_task)
    t2 = threading.Thread(target = log_worker)
    # t1.start()
    t2.start()
    for i in range(0, 3):
        add_task()
    print(threading.active_count())

if __name__ == '__main__':
    while True:
        start_thread(log_worker, daemon = True)
        command = input()
        command = command.split(' ')
        t = add_task(command)
        print(t)
    # for i in range(0, 3):
    #     t = start_thread(add_task)
    #     t.join()
    #     print(t)
