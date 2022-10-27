import math
import time

class rootfinder():
# tested
  def getPolyNomial(self, stringPol):
    self.polynomial = stringPol
    self.zeros = False
    for i in self.polynomial:
      if i[0] == 0 :
        self.zeros == True
    if self.zeros == False and len(self.polynomial) != 1:
      self.min = self.polynomial[0][0]
      for i in self.polynomial:
        if i[0] < self.min:
          self.min = i[0]
      for i in range(len(self.polynomial)):
        self.polynomial[i][0] -= self.min 
    for i in range(len(self.polynomial)):
      self.polynomial[i][1] = self.polynomial[i][1] / self.polynomial[0][1]
    
  # tested
  def Radius(self):
    self.maxorder = 0
    maxcoefficient = 0
    mincoefficient = 0
    for orders in self.polynomial:
      if float(orders[0]) > float(self.maxorder):
        self.maxorder = orders[0]
        maxcoefficient = orders[1]
      if orders[0] == 0:
        mincoefficient = orders[1]
    return float((abs(mincoefficient / maxcoefficient))**(1/self.maxorder))
# tested
  def PointMaker(self):
    self.X = []
    r = self.Radius()
    theta = 2*math.pi / self.maxorder
    c = theta / 4
    for i in range(self.maxorder):
      self.X.append(complex(r*math.cos((i)*theta+c),r*math.sin((i)*theta+c)))
    return [theta,c,self.X]
# tested
  def PX(self, index):
    sum = 0
    for i in self.polynomial:
      sum = sum + i[1]*((self.X[index])**i[0])
    return sum
#tested
  def divide(self, index):
    multi = complex(1,0)
    for i in range(len(self.X)):
      if i != index:
        multi = multi * (self.X[index] - self.X[i])
    return multi
  
#tested
  def RootWithError(self, error):
    if (len(self.polynomial) == 1 and self.polynomial[0][0] !=0) or len(self.polynomial) == 0:
      return 0
    if len(self.polynomial) == 1 and self.polynomial[0][0] ==0:
      return "it doesnt have roots"
    self.PointMaker()
    start_time=time.time()
    def checker(root1,root2,n,err):
      for i in range(len(root1)):
        if abs(root1[i] - root2[i]) <= (err / (n-1)):

          return False
      return True
    def copy(list):
      cop = []
      for i in list:
        cop.append(i)
      return cop
    counter = 1
    Continue = True
    while Continue:
      fakeroots = copy(self.X)

      counter += 1
      for j in range(len(self.X)):
        self.X[j] = fakeroots[j] - self.PX(j) /(self.divide(j))

      Continue = checker(fakeroots, self.X, counter, error)
    for i in range(self.min):
      self.X.append(0)
    def bias(roots1,roots2,n):
      errors = []
      for i in range(len(roots1)):
        errors.append((n-1)*abs(roots1[i] - roots2[i]))
      return errors
    for i in range(counter):
      fakeroots = copy(self.X)
      for j in range(len(self.X)):
        self.X[j] = fakeroots[j] - self.PX(j) /(self.divide(j))
      
    self.X[j] = fakeroots[j] - self.PX(j) /(self.divide(j))
    biass =  bias(self.X,fakeroots,counter)
  
    return [self.X,counter,biass,"--- %s seconds ---" % (time.time() - start_time)]
  def RootWithMaxError(self, error):
    if (len(self.polynomial) == 1 and self.polynomial[0][0] !=0) or len(self.polynomial) == 0:
      return 0
    if len(self.polynomial) == 1 and self.polynomial[0][0] ==0:
      return "it doesnt have roots"
    self.PointMaker()
    start_time=time.time()
    def checker(root1,root2,n,err):
      for i in range(len(root1)):
        if abs(root1[i] - root2[i]) <= (err / (n-1)):

          return False
      return True
    def copy(list):
      cop = []
      for i in list:
        cop.append(i)
      return cop
    counter = 1
    Continue = True
    while Continue:
      fakeroots = copy(self.X)

      counter += 1
      for j in range(len(self.X)):
        self.X[j] = fakeroots[j] - self.PX(j) /(self.divide(j))

      Continue = checker(fakeroots, self.X, counter, error)
    for i in range(self.min):
      self.X.append(0)
    def bias(roots1,roots2,n):
      errors = []
      for i in range(len(roots1)):
        errors.append((n-1)*abs(roots1[i] - roots2[i]))
      return errors
    for i in range(counter):
      fakeroots = copy(self.X)
      for j in range(len(self.X)):
        self.X[j] = fakeroots[j] - self.PX(j) /(self.divide(j))
      
    self.X[j] = fakeroots[j] - self.PX(j) /(self.divide(j))
    biass =  bias(self.X,fakeroots,counter)
    
    return [self.X,counter,biass,max(biass),"--- %s seconds ---" % (time.time() - start_time)]
  def RootWithNumber(self, num):
    if (len(self.polynomial) == 1 and self.polynomial[0][0] !=0) or len(self.polynomial) == 0:
      return 0
    if len(self.polynomial) == 1 and self.polynomial[0][0] ==0:
      return "it doesnt have roots"
    self.PointMaker()
    start_time = time.time()
    def copy(list):
      cop = []
      for i in list:
        cop.append(i)
      return cop

    def bias(roots1,roots2,n):
      errors = []
      for i in range(len(roots1)):
        errors.append((n-1)*abs(roots1[i] - roots2[i]))
      return errors
    for i in range(num):
      fakeroots = copy(self.X)
      for j in range(len(self.X)):
        self.X[j] = fakeroots[j] - self.PX(j) /(self.divide(j))
      
    self.X[j] = fakeroots[j] - self.PX(j) /(self.divide(j))
    biass =  bias(self.X,fakeroots,num)
    for i in range(self.min):
      self.X.append(0)
    return[self.X,biass,max(biass),"--- %s seconds ---" % (time.time() - start_time)]


m = rootfinder()

#m.getPolyNomial([[7,1],[6,-5],[5,7],[4,-6],[3,11],[2,-7],[1,5],[0,-6]])
#print(m.RootWithError(1e-15))

#m.getPolyNomial([[8,1],[7,0],[6,-1],[5,0.1],[4,-4],[3,1],[2,6],[1,-1],[0,-1]])
#print(m.RootWithError(1e-15))

m.getPolyNomial([[2,1],[1,0],[0,1]])
m.getPolyNomial([[4,1],[3,-1],[2,-3],[1,1],[0,1]])
print(m.RootWithError(1e-15))
print(m.RootWithMaxError(1e-15))

print(m.RootWithNumber(8))

