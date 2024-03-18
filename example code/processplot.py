import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_csv("data.csv")
print(data)

D=data.to_numpy()
t=D[:,0]
x=D[:,1]
y=D[:,2]
z=D[:,3] /9.81 

#plt.plot(t,x)
#plt.plot(t,y)
plt.plot(t,z)
plt.legend(["Force Z"])
plt.ylabel("Force (g)")
plt.xlabel("Time (s)")
plt.xlim([min(t),max(t)])
#plt.savefig('basic.png')
plt.show()
