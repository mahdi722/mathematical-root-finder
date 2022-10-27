import time

class vatari():
  def getPolyNomial(self, stringPol):
    self.polynomial = stringPol
    self.zero = 0
    while self.minco(self.polynomial) != 0:
      self.zero += 1
      for i in range(len(self.polynomial)):
        self.polynomial[i][0] -= 1
    
#tested
  def minco(self, poly):
    minco = poly[0][0]
    for i in poly:
      if i[0] < minco:
        minco = i[0]
    return minco
  def maxco(self, poly):
    coefficient = 0
    maxorder = 0
    for item in poly:
      if item[0] > maxorder:
        maxorder = item[0]
        coefficient = item[1]
    return [maxorder,coefficient]
#tested
  def roots2(self, poly):
    return [(-poly[1][1] - (poly[1][1]**2 - 4*poly[0][1] * poly[2][1])** (1/2))/(2*poly[0][1]),
                (-poly[1][1] + (poly[1][1]**2 - 4*poly[0][1] * poly[2][1])**(1/2))/(2*poly[0][1])]

#tested
  def polyx(self, poly, x):
    sum = 0
    for i in poly: 
     sum = sum + (i[1]*(float(x**i[0])))
    return sum

#tested
  def factoriel(self,n):

    fact=1
    for i in range(1,n+1):
      fact = fact*i
    return fact
#tested

  def diff(self, poly):

    def checker(pol):
      if pol[0] == 0:
        return False
      return True
    diff = []
    for i in poly:
      if checker(i):
        diff.append([i[0]-1,i[1]*self.factoriel(i[0])/self.factoriel(i[0]-1)])
    return diff


##############################################################tested
  def Mfinder(self,x0,x1,poly):
    maxorder,maxcoefficient = self.maxco(poly)[0],self.maxco(poly)[1]
    ## an > 0 , n %2 == 0 or an < 0 , n %2 != 0
    if (maxcoefficient > 0 and maxorder % 2 == 0 ) or (maxcoefficient < 0 and maxorder % 2 != 0):
      x00 = x0
      m = 10**(-5)
      n = 0
      while True:
        if self.polyx(poly,x00)>0:
          break
        if n == 100:
          m *= 10
          n = 0
        n += 1
        x00 -= m
    # an > 0 , n%2 != 0 or an < 0 , n%2==0
    elif (maxcoefficient > 0 and maxorder % 2 != 0 ) or (maxcoefficient < 0 and maxorder % 2 == 0):
      x00 = x0
      m = 10**(-5)
      n = 0
      while True:
        if self.polyx(poly,x00)<0:
          break
        if n == 100:
          m *= 10
          n = 0
        n += 1
        x00 -= m

  # an > 0 
    if maxcoefficient > 0 :
      x11= x1
      m = 10 **(-5)
      n = 0
      while True:
        if self.polyx(poly,x11) > 0:
          break
        if n == 100:
          n=0
          m *= 10
        n+=1
        x11 += m
    
  #an<0
    if maxcoefficient < 0:
      x11= x1
      m = 10 **(-5)
      n = 0
      while True:
        if self.polyx(poly,x11) < 0:
          break
        if n == 100:
          n=0
          m *= 10
        n+=1
        x11 += m 
    if x00 == x11:
      x11 += 0.1
    return (x00,x11)
################################################################ tested
  
  def secant(self, x0, x1, n , P):
    
    for i in range(n-1):
      if self.polyx(P,x1)-self.polyx(P,x0) != 0 :
        newx = (x0 * self.polyx(P,x1) - x1 * self.polyx(P,x0))/(self.polyx(P,x1)-self.polyx(P,x0))
        x0 = x1 
        x1 = newx
      else:
        break
    return x1
################################################################ fixed
  def polymaker(self,poly):
    roots = []
    roots.append(poly)
    while self.maxco(roots[-1])[0] != 2:
      roots.append(self.diff(roots[-1]))

    return roots
  ###################3
  def swipper(self, poly, list):
    m = 0
    for i in range(1,len(list)):
      if self.polyx(poly,list[m]) * self.polyx(poly,list[i]) < 0:
        m = i
      else:
        if self.polyx(poly, list[m]) == 0:
          m = i
        if self.polyx(poly, list[i]) != 0:
          list[i] = None
        
    while True:
      if None not in list:
        break
      list.remove(None)
    return list



  def bounderieswithn(self, poly,n):
    error = []
    d = []
    h = []
    start_time = time.time()
    if self.maxco(poly)[0] == 2:
     return self.roots2(poly)
    if self.maxco(poly)[0] == 1:
      return 0 - (poly[0][1] /poly[1][1])
    allpol = self.polymaker(poly)
    allroots = []
    prts = self.roots2(allpol[-1])
    del allpol[-1]
    dualroots = self.Mfinder(prts[0],prts[1],allpol[-1])
    prts.insert(0,dualroots[0])
    prts.append(dualroots[1])
    del dualroots
    allroots.append(prts)
    
    prtslen = len(allpol)
    
    for i in range(prtslen):
      prts = []
      for j in range(len(allroots[-1])-1):
        if j+1 == len(allroots[-1]) :
          break
        else:
          if  i <= prtslen -1:
            prts.append(self.secant(allroots[-1][j],allroots[-1][j+1],300,allpol[-1]))
          else:
            prts.append(self.secant(allroots[-1][j],allroots[-1][j+1],n,allpol[-1]))
      if i != prtslen - 1 :
        del allpol[-1]
        if len(prts) != 0:
          dualroots = self.Mfinder(prts[0],prts[-1],allpol[-1])
          prts.insert(0,dualroots[0])
          prts.append(dualroots[1]) 
        prts = self.swipper(allpol[-1],prts)
      allroots.append(prts)
      

    if self.zero != 0:
      allroots[-1].append(0)
    for i in range(len(allroots[-1])):
      error.append(self.polyx(self.polynomial,allroots[-1][i]))
    return [allroots[-1],error,"sec : ",(time.time() - start_time)]

  def secant(self, x0, x1, n , P):
    for i in range(n-1):
      if self.polyx(P,x1)-self.polyx(P,x0) != 0 :
        newx = (x0 * self.polyx(P,x1) - x1 * self.polyx(P,x0))/(self.polyx(P,x1)-self.polyx(P,x0))
        x0 = x1 
        x1 = newx
      else:
        break
    return x1
  def secantwitherr(self, x0, x1, err, P):
    counter = 1
    if self.polyx(P,x1)-self.polyx(P,x0) != 0 :
      newx = (x0 * self.polyx(P,x1) - x1 * self.polyx(P,x0))/(self.polyx(P,x1)-self.polyx(P,x0))
      x0 = x1 
      x1 = newx
    else:
      return[x1,1]
    while True:
      if abs(self.polyx(P,x1)) > err:
        newx = (x0 * self.polyx(P,x1) - x1 * self.polyx(P,x0))/(self.polyx(P,x1)-self.polyx(P,x0))
        x0 = x1 
        x1 = newx
        counter += 1
      else: 
        break
    return [x1,[counter]]
  def bounderieswitherr(self, poly, err):
    error = []
    allpol = self.polymaker(poly)
    allroots = []
    counter = []
    start_time = time.time()
    if self.maxco(poly)[0] == 2:
     return self.roots2(poly)
    if self.maxco(poly)[0] == 1:
      return 0 - (poly[0][1] /poly[1][1])
    prts = self.roots2(allpol[-1])
    del allpol[-1]
    dualroots = self.Mfinder(prts[0],prts[1],allpol[-1])
    prts.insert(0,dualroots[0])
    prts.append(dualroots[1])
    del dualroots
    allroots.append(prts)
    
    prtslen = len(allpol)
    
    for i in range(prtslen):
      prts = []
      cprts = []
      for j in range(len(allroots[-1])-1):
        if j+1 == len(allroots[-1]) :
          break
        else:
          if i < prtslen -1:
            res = self.secant(allroots[-1][j],allroots[-1][j+1],300,allpol[-1])
            
            prts.append(res) 
          else:
            res = self.secantwitherr(allroots[-1][j],allroots[-1][j+1],err,allpol[-1])
          
            cprts.append(res[1])
            prts.append(res[0])
      if i != prtslen - 1 :
        del allpol[-1]
        if len(prts) != 0:
          dualroots = self.Mfinder(prts[0],prts[-1],allpol[-1])
          prts.insert(0,dualroots[0])
          prts.append(dualroots[1]) 
        
        prts = self.swipper(allpol[-1],prts)
      counter.append(cprts)
      allroots.append(prts)
      
    
    if self.zero != 0:
      allroots[-1].append(0)
    errr = []
    
    for i in allroots[-1]:
      errr.append(self.polyx(allpol[0],i))
    return [allroots[-1],counter[-1],errr,"sec : ",(time.time() - start_time)]
  def bounderiesmaxerr(self, poly, err):
    error = []
    d = []
    h = []
    start_time = time.time()
    if self.maxco(poly)[0] == 2:
     return self.roots2(poly)
    if self.maxco(poly)[0] == 1:
      return 0 - (poly[0][1] /poly[1][1])
    allpol = self.polymaker(poly)
    allroots = []
    counter = []
    prts = self.roots2(allpol[-1])
    del allpol[-1]
    dualroots = self.Mfinder(prts[0],prts[1],allpol[-1])
    prts.insert(0,dualroots[0])
    prts.append(dualroots[1])
    del dualroots
    allroots.append(prts)
    
    prtslen = len(allpol)
    
    for i in range(prtslen):
      prts = []
      cprts = []
      for j in range(len(allroots[-1])-1):
        if j+1 == len(allroots[-1]) :
          break
        else:
          if i < prtslen -1:
            res = self.secant(allroots[-1][j],allroots[-1][j+1],300,allpol[-1])
            
            prts.append(res) 
          else:
            res = self.secantwitherr(allroots[-1][j],allroots[-1][j+1],err,allpol[-1])
          
            cprts.append(res[1])
            prts.append(res[0])
      if i != prtslen - 1 :
        del allpol[-1]
        if len(prts) != 0:
          dualroots = self.Mfinder(prts[0],prts[-1],allpol[-1])
          prts.insert(0,dualroots[0])
          prts.append(dualroots[1]) 
        
        prts = self.swipper(allpol[-1],prts)
      counter.append(cprts)
      allroots.append(prts)
      
    
    if self.zero != 0:
      allroots[-1].append(0)
    errr = []
    
    for i in allroots[-1]:
      errr.append(self.polyx(allpol[0],i))
    return [allroots[-1],"eerrr",max(errr),counter[-1],"sec : ",(time.time() - start_time)]

  def final(self):
    maxco = self.maxco(self.polynomial)
    # tested
    if maxco[0] == 0:
      return "none"
    elif maxco[0] == 1:
      return 0 - (self.polynomial[0][1] /self.polynomial[1][1])
    elif maxco[0] == 2:
      if self.polynomial[1][1]**2 - self.polynomial[0][1] * self.polynomial[2][1] < 0 :
        return "it has no real roots"
      else:
        return self.roots2(self.polynomial)
    elif maxco[0]>=3:
      return self.bounderieswithn(self.polynomial)
###############################################################################################################



m = vatari()
#print(m.bounderies([[7,1],[6,-5],[5,7],[4,-6],[3,11],[2,-7],[1,5],[0,-6]]))
#print(m.bounderies([[8,1],[7,0],[6,-1],[5,0.1],[4,-4],[3,1],[2,6],[1,-1],[0,-1]]))
#print(m.bounderies([[4,1],[3,-1],[2,-3],[1,1],[0,1]]))
#print(m.bounderies([[4,1],[3,-1],[2,-3],[1,1]]))
m.getPolyNomial([[4,1],[3,-1],[2,-3],[1,1],[0,1]])

print(m.bounderieswitherr([[8,1],[7,0],[6,-1],[5,0.1],[4,-4],[3,1],[2,6],[1,-1],[0,-1]],1e-14))
print(m.bounderieswitherr([[7,1],[6,-5],[5,7],[4,-6],[3,11],[2,-7],[1,5],[0,-6]],1e-14))
print(m.bounderieswitherr([[4,1],[3,-1],[2,-3],[1,1],[0,1]],1e-14))
