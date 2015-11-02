import time

with open('sample.txt', 'r') as f:
  i = 0
  while True:
    i+=1
    s = f.read()
    if s=="":
      print("noget : "+str(i))
   # else:
      #print(s)
   #print(f.read())
    f.seek(0)
    time.sleep(0.01)
f.closed
