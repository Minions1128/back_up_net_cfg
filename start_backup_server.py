import os
import re
import sys
import time
import socket
import zipfile
import threading

from Queue import Queue

from back_lib.errors import AuthenticationError
from back_lib._s_device import TDevice
from back_lib._s_device import DevInfo
from back_lib.send_mail import SendEmail
from back_lib._s_device import proc_queue

sys.path.append('./gen-py')

from _queue import _Queue
from _queue.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from back_lib.ctnt import RECEIVER_LIST
from back_lib.ctnt import THRIFT_IP, THRIFT_PORT


class BackupDevInfoHandler(object):

    def __init__(self, ip_list):
        super(BackupDevInfoHandler, self).__init__()
        self.ip_list = ip_list
        self.total_count = len(ip_list)
        self.fail_count = 0
        self.succ_count = 0
        self.logs = {}
        self.proc_count = 0
        os.system('rm -rf ./_config/*')
        os.system('mkdir ./_config/temp')

    def _login(self, username, password):
        self.username = username
        self.password = password

    def get_all_dev_info(self):
        sum_count = len(self.ip_list)
        for ip in self.ip_list:
            proc_queue.put(ip)
        for i in range(sum_count/3):
            self.proc_count += 1
            t = threading.Thread(target=self.get_one_dev_config)
            t.start()
        while self.proc_count > 0:
            pass
        summary_info = {
            'total_count':self.total_count,
            'fail_count':self.fail_count,
            'succ_count':self.succ_count
        }
        summary = self.get_total_info(summary_info, self.logs)
        log_path = './_config/temp/_log.txt'
        with open(log_path, 'w+') as f_log:
            f_log.write(summary)

    def get_one_dev_config(self):
        """ get one device configuration.
            return the 'show run' result
            arguments:
            ip: the ip address of this device
            username & password: 
                the username and password can
                telnet to the device."""
        while True:
            print proc_queue._queue, proc_queue._len
            if proc_queue.empty():
                self.proc_count -= 1
                break
            ip = proc_queue.get()
            self.logs.setdefault(ip, {})
            info = {'ip':ip}
            if self._is_ip_addr(ip):
                dev_info = self.get_dev(ip)
                if dev_info._is_succ:
                    self.succ_count += 1
                    path = './_config/temp/' + dev_info.hostname \
                        + '.' + ip + '.txt'
                    with open(path, 'w+') as f_cfg:
                        f_cfg.write(dev_info.config)
                else:
                    self.fail_count += 1
                    succ_flg = False
                info['log'] = dev_info.log
                info['status'] = dev_info._is_succ
            else:
                self.fail_count += 1
                info['log'] = ip, 'is bad ip address'
                info['status'] = False
            self.logs[ip] = info

    def get_dev(self, ip):
        device = TDevice(ip, self.password,
                self.username)
        try:
            device.t_connect()  #arg: timeout=10
            _s_log = "Logged into {} successfully".format(
                device.hostname)
            _is_succ = True
        except AuthenticationError as e:
            _s_log =  "Couldn't connect to {}: {}".format(
                ip, e.value)
            _is_succ = False
        except Exception as e:
            _s_log = "Couldn't connect to {}: {}.".format(
                ip, str(e))
            _is_succ = False
        except:
            _s_log = "Couldn't connect to {}.".format(ip)
            _is_succ = False
        dev_info = DevInfo(_is_succ, ip, _s_log)
        if _is_succ:
            dev_info.set_hostname(device.hostname)
            cfg = device.cmd('show run')
            dev_info.show_run(cfg)
        return dev_info

    @staticmethod
    def _is_ip_addr(src):
        if not src or not type(src) in [str, unicode]:
            return False
        re_str = ur"^([1-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])){3}$"
        ptn = re.compile(re_str, flags=re.S|re.I|re.M)
        if ptn.findall(src):
            return True
        return False

    def get_total_info(self, total_info, details):
        summary = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
        summary += "\n{} login successfully.".format(self.username)
        summary += '\n\n================================================='
        summary += '\n================= SUMMARY START ================='
        summary += '\n================================================='
        summary += '\n\nTotal: {}, Successful: {}, Fail: {}.'.format(
            total_info['total_count'], total_info['succ_count'],
            total_info['fail_count'])

        summary += '\n\n-------------- SUCCESSFUL --------------\n\n'
        l_succ = []
        for ip in details:
            if details[ip]['status'] == True:
                l_succ.append(ip)
        summary += str(l_succ)

        summary += '\n\n----------------- FAIL -----------------\n\n'
        l_fail = []
        for ip in details:
            if details[ip]['status'] == False:
                l_fail.append(ip)
                summary = summary + str(details[ip]['log']) + '\n'
        summary += '\n\n'
        summary += str(l_fail)
        summary += '\n\n================================================='
        summary += '\n================== SUMMARY END =================='
        summary += '\n=================================================\n'
        print summary
        return summary

    def add_dirfile(self):
        path = './_config/net_dev_config_.zip'
        f = zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED)
        startdir = "./_config/temp"
        for dirpath, dirnames, filenames in os.walk(startdir):
            for filename in filenames:
                cmd = 'cp ' + os.path.join(dirpath,filename) \
                    + ' ./' + filename
                os.system(cmd)
                f.write('./'+filename)
                cmd = 'rm -rf ./' + filename
                os.system(cmd)
        f.close()

    def send_mail(self, receiver_list):
        SendEmail(receivers_list=receiver_list)

    def _close(self):
        os.system('rm -rf ./_config/*')


class _QueueHandler(object):
    def __init__(self):
        self._q = Queue()

    def put_queue(self, u, p, ips, r_s):
        self._q.put((u, p, ips, r_s))
        return 'yes'

    def get_queue(self):
        return self._q.get()


if __name__ == '__main__':

    handler = _QueueHandler()

    # get the thrift queue info
    processor = _Queue.Processor(handler)
    transport = TSocket.TServerSocket(THRIFT_IP, THRIFT_PORT)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    print "Starting back_up in python..."

    new_thread = threading.Thread(target=server.serve)
    new_thread.start()

    while True:        
        u, p, ips, r_s = handler.get_queue()
        t = time.time()
        _proc = BackupDevInfoHandler(ips)
        _proc._login(u, p)
        print 'login succ'
        _proc.get_all_dev_info()
        print 'get all dev info'
        _proc.add_dirfile()
        print 'packet zipped'
        _proc.send_mail(r_s)
        print 'send mail'
        _proc._close()
        print 'close...', time.time() - t

    print "done!"
