#!/usr/bin/env python3

class Diary:
    def __init__(self,fileName=None):
        if not fileName:
            fileName=input("일기를 저장할 파일 이름을 입력하세요:")
        self.fileName=fileName
        self.f=None
    def open(self,mode='w+'): # open file
        try:
            self.file=open(self.fileName,mode)
        except OSError as e: # Error handling
            sys.stderr.write("I/O error({0}): {1}".format(e.errno, e.strerror))
            self.file.close() # Close
            self.file=None
    def close(self): # Close file
        if self.file != None:
            self.file.close()
    def __exit__(self): # dtor
        self.close()
    def write(self):
        self.file.write(.....) # 이 안에 날짜가 저장되도록 적절한 코드를.
        # 위의 예시를 참고하여 사용자에게 일기 내용을 입력을 받아 저장하도록 해 보세요.
        self.file.flush()

if __name__=='__main__':
    dr=Diary()
    dr.open()
    dr.write()
    dr.close()
