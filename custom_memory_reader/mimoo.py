# scans PID for utf-8 string with option to stop on first occurence
# adjusted code taken from Awesometech here https://python-forum.io/thread-5517.html
# Apachi -me- slightly adjusted the code from https://medium.com/@algolithics/scanning-windows-memory-with-python-memory-string-detection-6b80e1dac1d0

import ctypes
from ctypes.wintypes import WORD, DWORD, LPVOID
import psutil
import sys, os
import psutil
import pprint
import time
class SYSTEM_INFO(ctypes.Structure):
 """https://msdn.microsoft.com/en-us/library/ms724958"""
 class _U(ctypes.Union):
  class _S(ctypes.Structure):
   _fields_ = (('wProcessorArchitecture', WORD),
      ('wReserved', WORD))
  _fields_ = (('dwOemId', DWORD), # obsolete
     ('_s', _S))
  _anonymous_ = ('_s',)
 
 
 if ctypes.sizeof(ctypes.c_void_p) == ctypes.sizeof(ctypes.c_ulonglong):
  DWORD_PTR = ctypes.c_ulonglong
 elif ctypes.sizeof(ctypes.c_void_p) == ctypes.sizeof(ctypes.c_ulong):
  DWORD_PTR = ctypes.c_ulong
 
 _fields_ = (('_u', _U),
    ('dwPageSize', DWORD),
    ('lpMinimumApplicationAddress', LPVOID),
    ('lpMaximumApplicationAddress', LPVOID),
    ('dwActiveProcessorMask',   DWORD_PTR),
    ('dwNumberOfProcessors', DWORD),
    ('dwProcessorType',   DWORD),
    ('dwAllocationGranularity', DWORD),
    ('wProcessorLevel', WORD),
    ('wProcessorRevision', WORD))
 _anonymous_ = ('_u',)

 
class MEMORY_BASIC_INFORMATION(ctypes.Structure):
 """https://msdn.microsoft.com/en-us/library/aa366775"""
 PVOID = LPVOID
 SIZE_T = ctypes.c_size_t
 _fields_ = (('BaseAddress', PVOID),
    ('AllocationBase', PVOID),
    ('AllocationProtect', DWORD),
    ('RegionSize', SIZE_T),
    ('State',   DWORD),
    ('Protect', DWORD),
    ('Type', DWORD))
 
 
 
 

def main(PID = os.getpid(), FIND_STR='ąsdf1234', _exit_on_first_match=True,_dump_all_to_file_=False,_dfile_name_="dumb.txt"):

 findstr= bytearray(FIND_STR.encode('utf-8'))
 
 print(f'\n*** Searching {FIND_STR} in PID {PID} _exit_on_first_match {_exit_on_first_match}\n' )
 
 LPSYSTEM_INFO = ctypes.POINTER(SYSTEM_INFO) ##PMEMORY_BASIC_INFORMATION = ctypes.POINTER(MEMORY_BASIC_INFORMATION)  
  
 Kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
 Kernel32.GetSystemInfo.restype = None
 Kernel32.GetSystemInfo.argtypes = (LPSYSTEM_INFO,)
 ReadProcessMemory = Kernel32.ReadProcessMemory
  
 sysinfo = SYSTEM_INFO()
 Kernel32.GetSystemInfo(ctypes.byref(sysinfo))
 start_addr=sysinfo.lpMinimumApplicationAddress
 current_address = sysinfo.lpMinimumApplicationAddress
 end_address = sysinfo.lpMaximumApplicationAddress
 
 
 PROCESS_QUERY_INFORMATION = 0x0400
 PROCESS_VM_READ = 0x0010
 MEM_COMMIT = 0x00001000;
 PAGE_READWRITE = 0x04;
  
 Process = Kernel32.OpenProcess(PROCESS_QUERY_INFORMATION|PROCESS_VM_READ, False, PID) # print('process:', Process)

 mbi = MEMORY_BASIC_INFORMATION() 
 
 buffer = ctypes.c_char() #c_double() ##buffer = ctypes.c_uint()
 nread = ctypes.c_size_t() #SIZE_T()
  
 # start = ctypes.c_void_p(mbi.BaseAddress)
 msg="Area to scan bounds {} to {}".format(str(hex(current_address)),str(hex(end_address)))
 print(msg)
 
 if _dump_all_to_file_:
  dfile=open(_dfile_name_,'w')
  dfile.write((f'[#] Scanning {str(PID)}:'))
  dfile.write(msg)
  dfile.write("====================================")
  dumb_content=[]
 ci=0
 count_occur=0
 
 while current_address < end_address:
  current_address_ctypes=ctypes.c_void_p(current_address) 
  _k=Kernel32.VirtualQueryEx(Process,  current_address_ctypes, ctypes.byref(mbi), ctypes.sizeof(mbi)) # read cur region to mbi
  if mbi.Protect == PAGE_READWRITE and mbi.State == MEM_COMMIT : # print('This region can be scanned!',index,end, end-index)
   index = current_address
   end = current_address + mbi.RegionSize
   
   ci=0
   vi=[]
   f_ind=-1
   while index < end: # index -> ctypes.c_void_p(index) ?
    rm=ReadProcessMemory(Process, ctypes.c_void_p(index), ctypes.byref(buffer),  ctypes.sizeof(buffer), ctypes.byref(nread)) # read cur region bytes to bugger
    # print('rm',rm)
    if _dump_all_to_file_:
     dumb_content.append(buffer.value)
    if rm>0 :
     _x=findstr[ci].to_bytes(1, 'little')
     if buffer.value==_x:
      if ci==0: f_ind=index
      vi.append(buffer.value)
      ci+=1
      if ci==len(findstr):
       count_occur+=1
       print(f'MATCHED [{count_occur}] STRING between indexes {f_ind} and {index}') #, ,, b''.join(vi).decode('utf-8'))
       if _exit_on_first_match:
        # current_address = end_address
        print('\texiting on _exit_on_first_match',_exit_on_first_match)
        return
        
       else: ci, f_ind, vi = 0, -1, [] 
     else: ci, f_ind, vi=0, -1, [] 
    else: ci, f_ind, vi = 0, -1, [] 
     
    index += ctypes.sizeof(buffer) 
     
  
  
  print(f"\tProgress done {current_address-start_addr} {round(100*(current_address-start_addr)/(end_address-start_addr))}%, left {end_address-current_address}, this iter did {mbi.RegionSize}") #{round(100*(end_address-current_address)/(end_address-start_addr))}
  
  current_address += mbi.RegionSize
 print(("="*30).encode())
 #print(dumb_content)
 #pprint.pprint(dumb_content)
 if _dump_all_to_file_:
  bcont=b''.join(dumb_content)
  #decoded_string = bcont.decode('utf-8')
  #dfile.write(decoded_string)
  dfile.close()
 write_bytes_list_to_plain_hex(dumb_content)
 print('hex content written out')
def write_bytes_list_to_plain_hex(bls,file_name='plain_hex'):
 '''takes a list of bytes obj , probably just a byte, convert to hex string '''
 with open(file_name,'wb') as f:
  bytes_data=b''
  for b in bls:
   if b==b'\x00':
    continue
   bytes_data+=b
  f.write(bytes_data)
def get_pid(name,print_enc=False):
  for proc in psutil.process_iter():
      if print_enc:
          print(proc.name())
      if proc.name() == name:
          return proc

if __name__ == '__main__':
 if len(sys.argv)== 1:
     print('Please add the processname as an arg e.g: process_name.exe')
     sys.exit()
 process_name = sys.argv[1]
 print('sleeping for 10 seconds before initiating the digital bomb')
 time.sleep(10)
 print('Fire in the HOLEE!')
 process=get_pid(process_name)
 pid=process.pid
 s="HWID"

 main(pid,s,_exit_on_first_match=False,_dump_all_to_file_=True)
 print('\n*** Finished scanning memory\n')
 
