import socket            
s = socket.socket()        
print ("Socket successfully created")
port = 3389              
s.bind(('', port))        
print ("socket binded to %s" %(port))
s.listen(5)    
print ("socket is listening")           
while True:
  c, addr = s.accept()    
  print ('Got connection from', addr )
  c.send('Thank you for connecting'.encode())
  print(c.recv(1024).decode())
  c.close()
  break
