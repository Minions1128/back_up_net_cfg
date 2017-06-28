
import telnetlib

from device import Device
from errors import AuthenticationError
from ctnt import ASA_LIST


class TDevice(Device):

    def __init__(self, *args, **kwargs):
        super(TDevice, self).__init__(*args, **kwargs)

    def t_connect(self, host=None, port=23, timeout=10):
        if host is None:
            host = self.host
        self._connection = telnetlib.Telnet(host, port, timeout)
        self.t_authenticate(timeout)
        self._get_hostname()
        if self.host in ASA_LIST:
            '''if device type is ASA, the command is using below.'''
            self.cmd("terminal pager 0")
        else:
            self.cmd("terminal length 0")
        
        self.connected = True

    def t_authenticate(self, timeout=None):
        idx, match, text = self.expect(['sername:', 'assword:', 'login:'], timeout)
        if match is None:
            raise AuthenticationError("Unable to get a prompt of username or password.", text)
        elif match.group().count(b'sername') > 0:
            if self.username is None:
                raise AuthenticationError("A username is required.")
            self.write(self.username+"\n")
            idx, match, text = self.expect(['assword:'], timeout)
            if match is None:
                raise AuthenticationError("Unexpected text when trying to enter password", text)
            elif match.group().count(b'assword'):
                self.write(self.password+"\n")
            idx, match, text = self.expect(['#', '>', "Login invalid", "Authentication failed"], timeout)
            if match is None:
                raise AuthenticationError("Unexpected text post-login", text)
            elif b"invalid" in match.group() or b"failed" in match.group():
                raise AuthenticationError("Username or password are incorrect.")
            elif match.group().count(b'>'):
                self.write("enable 15\n")
                idx, match, text = self.expect(['assword:'], timeout)
                if match.group().count(b'assword'):
                    if self.host in ASA_LIST:
                        self.write("\n")
                    else:
                        self.write(self.enable_password+"\n")
                    idx, match, text = self.expect(['>', "Login invalid", "Authentication failed", '#'], timeout)
                    if match is None:
                        raise AuthenticationError("Unexpected text post-login", text)
                    elif match.group().count(b'>') or b"invalid" in match.group() or b"failed" in match.group():
                        raise AuthenticationError("Enable password is incorrect.", text)
        elif match.group().count(b'ogin') > 0:
            if self.username is None:
                raise AuthenticationError("A username is required.")
            self.write(self.username+"\n")
            idx, match, text = self.expect(['assword:'], timeout)
            if match is None:
                raise AuthenticationError("Unexpected text when trying to enter password", text)
            elif match.group().count(b'assword'):
                self.write(self.password+"\n")
            idx, match, text = self.expect(['#', "Login invalid", "Authentication failed"], timeout)
            if match is None:
                raise AuthenticationError("Unexpected text post-login", text)
            elif b"invalid" in match.group() or b"failed" in match.group():
                raise AuthenticationError("Username or password are incorrect.")
        elif match.group().count(b'assword:'):
            self.write(self.password+"\n")
            idx, match, text = self.expect(['#', "Login invalid", "Authentication failed"], timeout)
            if match is None:
                raise AuthenticationError("Unexpected text post-login", text)
            elif b"invalid" in match.group() or b"failed" in match.group():
                raise AuthenticationError("Username or password are incorrect.")
        else:
            raise AuthenticationError("Unable to get a login prompt")

class DevInfo(object):
    def __init__(self, state, ip, log):
        self._is_succ = state
        self.ip = ip
        self.log = log

    def set_hostname(self, hostname):
        self.hostname = hostname

    def show_run(self, cfg):
        self.config = cfg


class Queue(object):
    def __init__(self):
        self._len = 0
        self._queue = []

    def put(self, c):
        self._len += 1
        self._queue.append(c)

    def get(self):
        while self._len <= 0:
            pass
        self._len -= 1
        return self._queue.pop(0)

    def empty(self):
        if self._len > 0:
            return False
        elif self._len == 0:
            return True
        else:
            raise 'The length of queue is less than zero.'


proc_queue = Queue()
