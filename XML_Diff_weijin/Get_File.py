import os
import time
import ssh
def print_ts(message):
    print ("[%s] %s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message))
def run(interval, ip1,ip2,ip3, username, password, port):
    print_ts("-"*100)
    print_ts("Starting every %s seconds."%interval)
    print_ts("-"*100)
    while True:
        try:
            # sleep for the remaining seconds of interval
            time_remaining = interval-time.time()%interval
            print_ts("Sleeping until %s (%s seconds)..."%((time.ctime(time.time()+time_remaining)), time_remaining))
            time.sleep(time_remaining)
            print_ts("Starting command.")
            # execute the command
            ssh.get3str(ip1,ip2,ip3, username, password, port)
            print_ts("-"*100)

        except Exception as e:
            print(e)
# if __name__=="__main__":
#     interval = 5
#     command = r"ls"
#     run(interval, command)
if __name__ == '__main__':
    ip1 = '192.168.0.41'
    ip2 = '192.168.0.42'
    ip3 = '192.168.0.44'
    username = 'root'
    password = '111111'
    port = 22
    interval = 5
    run(interval,ip1,ip2,ip3, username, password, port)