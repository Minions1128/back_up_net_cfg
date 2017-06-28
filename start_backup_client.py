'''
send 1, the username, 2, user password, 
3, the ip address of backuped devices and
4, the recever mail list to THRIFT server
'''
import sys
import time
import getpass

sys.path.append('./gen-py')

from _queue import _Queue

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from back_lib.ctnt import THRIFT_IP, THRIFT_PORT
from back_lib.ctnt import RECEIVER_LIST
from back_lib.ctnt import AAA_USERNAME, AAA_PWD
from back_lib.ctnt import NET_DEV_IP

if __name__ == '__main__':
    try:
        # _user = AAA_USERNAME
        # _pwd = AAA_PWD
        _user = raw_input('Username: ')
        _pwd = getpass.getpass('Password: ')

        #testing start
        t = time.time()
        #testing end

        # to build the transport process
        transport = TSocket.TSocket(THRIFT_IP, THRIFT_PORT)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = _Queue.Client(protocol)
        transport.open()

        # put the info to queue
        print client.put_queue(_user, _pwd,
            NET_DEV_IP, RECEIVER_LIST)
    
        transport.close()
    
    except Thrift.TException, ex:
        print "%s" % (ex.message)

    #testing start
    print time.time() - t
    #testing end
