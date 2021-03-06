#
# Autogenerated by Thrift Compiler (0.9.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
from ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None


class Iface:
  def put_queue(self, user, pwd, ip_list, receiver_list):
    """
    Parameters:
     - user
     - pwd
     - ip_list
     - receiver_list
    """
    pass


class Client(Iface):
  def __init__(self, iprot, oprot=None):
    self._iprot = self._oprot = iprot
    if oprot is not None:
      self._oprot = oprot
    self._seqid = 0

  def put_queue(self, user, pwd, ip_list, receiver_list):
    """
    Parameters:
     - user
     - pwd
     - ip_list
     - receiver_list
    """
    self.send_put_queue(user, pwd, ip_list, receiver_list)
    return self.recv_put_queue()

  def send_put_queue(self, user, pwd, ip_list, receiver_list):
    self._oprot.writeMessageBegin('put_queue', TMessageType.CALL, self._seqid)
    args = put_queue_args()
    args.user = user
    args.pwd = pwd
    args.ip_list = ip_list
    args.receiver_list = receiver_list
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_put_queue(self, ):
    (fname, mtype, rseqid) = self._iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(self._iprot)
      self._iprot.readMessageEnd()
      raise x
    result = put_queue_result()
    result.read(self._iprot)
    self._iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    raise TApplicationException(TApplicationException.MISSING_RESULT, "put_queue failed: unknown result");


class Processor(Iface, TProcessor):
  def __init__(self, handler):
    self._handler = handler
    self._processMap = {}
    self._processMap["put_queue"] = Processor.process_put_queue

  def process(self, iprot, oprot):
    (name, type, seqid) = iprot.readMessageBegin()
    if name not in self._processMap:
      iprot.skip(TType.STRUCT)
      iprot.readMessageEnd()
      x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
      oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
      x.write(oprot)
      oprot.writeMessageEnd()
      oprot.trans.flush()
      return
    else:
      self._processMap[name](self, seqid, iprot, oprot)
    return True

  def process_put_queue(self, seqid, iprot, oprot):
    args = put_queue_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = put_queue_result()
    result.success = self._handler.put_queue(args.user, args.pwd, args.ip_list, args.receiver_list)
    oprot.writeMessageBegin("put_queue", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()


# HELPER FUNCTIONS AND STRUCTURES

class put_queue_args:
  """
  Attributes:
   - user
   - pwd
   - ip_list
   - receiver_list
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'user', None, None, ), # 1
    (2, TType.STRING, 'pwd', None, None, ), # 2
    (3, TType.SET, 'ip_list', (TType.STRING,None), None, ), # 3
    (4, TType.SET, 'receiver_list', (TType.STRING,None), None, ), # 4
  )

  def __init__(self, user=None, pwd=None, ip_list=None, receiver_list=None,):
    self.user = user
    self.pwd = pwd
    self.ip_list = ip_list
    self.receiver_list = receiver_list

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.user = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.pwd = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.SET:
          self.ip_list = set()
          (_etype3, _size0) = iprot.readSetBegin()
          for _i4 in xrange(_size0):
            _elem5 = iprot.readString();
            self.ip_list.add(_elem5)
          iprot.readSetEnd()
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.SET:
          self.receiver_list = set()
          (_etype9, _size6) = iprot.readSetBegin()
          for _i10 in xrange(_size6):
            _elem11 = iprot.readString();
            self.receiver_list.add(_elem11)
          iprot.readSetEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('put_queue_args')
    if self.user is not None:
      oprot.writeFieldBegin('user', TType.STRING, 1)
      oprot.writeString(self.user)
      oprot.writeFieldEnd()
    if self.pwd is not None:
      oprot.writeFieldBegin('pwd', TType.STRING, 2)
      oprot.writeString(self.pwd)
      oprot.writeFieldEnd()
    if self.ip_list is not None:
      oprot.writeFieldBegin('ip_list', TType.SET, 3)
      oprot.writeSetBegin(TType.STRING, len(self.ip_list))
      for iter12 in self.ip_list:
        oprot.writeString(iter12)
      oprot.writeSetEnd()
      oprot.writeFieldEnd()
    if self.receiver_list is not None:
      oprot.writeFieldBegin('receiver_list', TType.SET, 4)
      oprot.writeSetBegin(TType.STRING, len(self.receiver_list))
      for iter13 in self.receiver_list:
        oprot.writeString(iter13)
      oprot.writeSetEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class put_queue_result:
  """
  Attributes:
   - success
  """

  thrift_spec = (
    (0, TType.STRING, 'success', None, None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.STRING:
          self.success = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('put_queue_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.STRING, 0)
      oprot.writeString(self.success)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
