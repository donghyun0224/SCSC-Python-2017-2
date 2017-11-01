import sys
class DocWriter(object):
    def __init__(self,fileName): # ctor
        self.fileName=fileName
        self.file=None
    def open(self,mode='w+'): # open file
        try:
            self.file=open(self.fileName,mode)
        except OSError as e: # Error handling
            sys.stderr.write("I/O error({0}): {1}".format(e.errno, e.strerror))
            self.file.close() # Close
            self.file=None
    def write(self,data,colname1="",colname2="",printHeader=True,printType=False): # Write data
        if not self.file:
            raise IOError("File not opened!")
        if printType:
            self.file.write("Type:"+type(data).__name__)
        if printHeader:
            self.file.write(colname1+"\t"+colname2+"\n")
        for k,v in enumerate(data): # Print contents
            self.file.write("%s\t%s\n" % (k,v))
        self.file.flush() # flush
    def close(self): # Close file
        if self.file != None:
            self.file.close()
    def __exit__(self): # dtor
        self.close()

class TxtWriter(DocWriter):
    def write(self,data,colname1="",colname2="",printHeader=True,printType=False): # Method Overloading
        if not self.file:
            raise IOError("File not opened!")
        maxlen1=len(colname1)
        maxlen2=len(colname2)
        for k,v in enumerate(data): # Calculate column width
            maxlen1=max(maxlen1,len(str(k)))
            maxlen2=max(maxlen2,len(str(v)))
        fmtstr="%"+str(maxlen1)+"s %"+str(maxlen2)+"s\n" # Format string
        if printType:
            self.file.write(type(data).__name__+"\n") # Print file
        if printHeader:
            self.file.write(fmtstr % (colname1,colname2)) # Print header
        for pair in enumerate(data): # Print contents
            self.file.write(fmtstr % pair)
        self.file.write("---END---\n\n") # Print footer
        self.file.flush() # flush
        
class HTMLWriter(DocWriter):
    def __init__(self,fileName,pageTitle=""):
        super().__init__(fileName)
        self.pageTitle=pageTitle
        self.hasHeader=False
    def createHeader(self): # Added method: Creates HTML header
        if not self.file:
            raise IOError("File not opened!")
        if self.hasHeader:
            return
        self.hasHeader=True
        self.file.write("<!DOCTYPE html><html><head><title>"+self.pageTitle+"</title></head><body>\n")

    def write(self,data,colname1="",colname2="",printHeader=True,printType=False): # Method Overloading
        if not self.file:
            raise IOError("File not opened!")
        if not self.hasHeader:
            self.createHeader()
        self.file.write("<table border=\"1\",style=\"width:100%\">")
        if printType:
            self.file.write(type(data).__name__+"\n") # Print file
        if printHeader and (colname1 or colname2):
            self.file.write("<tr><th>"+colname1+"</th><th>"+colname2+"</th></tr>\n") # Print header
        for pair in enumerate(data): # Print contents
            self.file.write("<tr><td>%s</td><td>%s</td></tr>\n" % pair)
        self.file.write("</table><br><br>\n") # Print footer
        self.file.flush() # flush
    def close(self):
        self.file.write("\n</body></html>")
        super().close()
        hasHeader=False

if __name__=="__main__":
    drt=DocWriter("DRTST.TXT")
    drt.open()
    drt.write([1,2,3,4,5,6],"A","B")
    drt.close()
