<!-- Use marp to create presentation -->
<!-- Download : https://yhatt.github.io/marp/ -->

<!--- 패이지번호 표시 -->
<!-- page_number: true -->
<!-- 화면비율 16:9 -->
<!-- $size : 16:9 -->

# Python 신입 SiG: 상속

<small>Nov 1st/2017</small>

---

# 상속과 다형성, Operator Overloading

---

## 상속

- 한 클래스가 다른 클래스를 기초로 하여 만들어진 것.
- Derived class(subclass)가 base class(superclass)를 상속받아 member를 가지고 옴.
- 재사용성을 부여함.
- Subclass와 superclass는 is-a 관계임(e.g. circle is a shape, apple is a fruit).
  - 즉, superclass가 더 상위 개념을 나타내며, subclass는 하위 개념을 나타낸다.

---

### Python에서의 구현

Class를 정의할 때 다음과 같이 상속받을 수 있다.
```Python
class <Name of subclass>(<Name of superclass>):
    ...
    <member variables, methods>
    ...
```
모든 class를 정의할 때 상속을 사용하고 있음. 기본적으로 `object`를 상속받음.
```Python
class foo:
	__init__(self):
		self.bar="The quick brown fox jumps over the lazy dog."
```
는 사실
```Python
class foo(object):
	__init__(self):
		self.bar="The quick brown fox jumps over the lazy dog."
```
이다. 

---

## Method Overriding

- Method를 다시 정의하여 기존의 정의를 덮어쓴다.
- Superclass에서와 subclass에서 동작이 달라야 할 경우에 사용.
- Subclass는 superclass의 method가 아닌 overriding 된 method를 호출하게 된다.
- 그냥 다시 정의하면 된다.
  - 인자의 수까지 같아야 함.

예시
<small>
```Python
class Dog:
    ...
    def sound(self):
    	print("Bow wow")
    def sound(self,str) # Method overloading
    	print(str)
    ...
class Cat(Dog):
    ...
    def sound(self): # Method overriding
    	print("Meaw")
    ...
```
</small>

---

## `Super` 키워드

- Subclass에서 Superclass의 member를 불러온다.
- Overriding 된 method에서 원래 superclass의 내용이 필요할때 사용.
  - 예: 생성자

<span style="font-size: 99%;">

```Python
class Shape:
	def __init__(self,posx,posy):
		...
		self.posx=posx
		self.posy=posy
		...
	...
class Circle(Shape):
	def __init__(self,posx,posy,rad=0):
		super().__init__(posx,posy) # Superclass인 shape의 constructor 불러온다.
		self.radius=rad # Superclass에 정의 안된 radius에 대한 initialization
	...

```
</span>

---

## 예시: 리스트를 간단히 택스트로 출력하는 `DocWriter`
다형성에서도 사용할 예시이다.

```Python
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
```
Cont...

---

Cont....
```Python
    # Data 기록
    def write(self,data,colname1="",colname2="",printHeader=True,printType=False):
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
```

---

### 예시: 리스트를 예쁜 택스트로 출력하는 `TxtWriter`
상속받은 후 method overriding 이용하여 예쁘게 출력한다.
```Python
class TxtWriter(DocWriter):
    # Method Overloading
    def write(self,data,colname1="",colname2="",printHeader=True,printType=False):
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
```

---

### 예시: 리스트를 예쁜 택스트로 출력하는 `HTMLWriter`
상속받은 후 method overriding 이용하여 HTML로 출력한다.
```Python
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
        self.file.write("<!DOCTYPE html><html><head><title>"+self.pageTitle+
        "</title></head><body>\n")
```

---

```Python
    def write(self,data,colname1="",colname2="",printHeader=True,printType=False):
        if not self.file:
            raise IOError("File not opened!")
        if not self.hasHeader: # HTML header
            self.createHeader()
        self.file.write("<table border=\"1\",style=\"width:100%\">")
        if printType:
            self.file.write(type(data).__name__+"\n") # Print file
        if printHeader and (colname1 or colname2) : # Table header
            self.file.write("<tr><th>"+colname1+"</th><th>"+colname2+"</th></tr>\n")
        for pair in enumerate(data): # Print contents
            self.file.write("<tr><td>%s</td><td>%s</td></tr>\n" % pair)
        self.file.write("</table><br><br>\n") # Print table footer
        self.file.flush() # flush
    def close(self):
        self.file.write("\n</body></html>")
        super().close()
        hasHeader=False

```

---

## 다형성
 - 부모 자리에 자식 클래스를 넣으면?
   - 자식 클래스에는 부모로부터 상속받은 method나 변수가 있으므로 문제 없이 동작할 수 있다.
   - 객체지향 5원칙 중 하나인 Liskov substitution principle에 해당.
 - 위의 예시에서 `write`가 상속된다. 따라서, 부모인 `DocWriter` object를 받아서 `write`를 호출하는 경우 그 object가 `DocWriter`, `TxtWriter`, `HTMLWriter`임에 무관하게 데이터를 출력하는 동작을 똑같이 수행한다.
---

### 예시: 함수값 테이블 출력

<span style="font-size:90%;">

```Python
from docwriters import *
from math import sin,pi
def printFuncTable(dwrt,func,start,stop,step=1):
	val={i:func(i) for i in range(start,stop,step)}
	dwrt.write(val,"x","f(x)")
smpwr=DocWriter("simple.txt")
prtwr=TxtWriter("pretty.txt")
htmwr=HTMLWriter("tbl.html")
smpwr.open()
prtwr.open()
htmwr.open()
printFunctable(smpwr,sin,-pi,pi,0.2)
printFunctable(smpwr,sin,-pi,pi,0.2)
printFunctable(smpwr,sin,-pi,pi,0.2)
smpwr.close()
prtwr.close()
htmwr.close()
```

</span>
결과적으로 각각의 object를 이용하여sin함수 태이블이 생성된다.

---
