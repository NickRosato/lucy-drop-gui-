import matplotlib.pyplot as plt
import math
x = [1,2,3,4,5]
y = [1000, 1002, 1001, 1003, 1005]
low = min(y)
high = max(y)
plt.ylim([math.ceil(low-0.5*(high-low)), math.ceil(high+0.5*(high-low))])
plt.bar(x,y) 
plt.show()
