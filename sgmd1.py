import numpy as np
input = np.linspace(-10, 10, 100)
#print(input)

def sigmoid(x):  
    return 1/(1+np.exp(-x))

from matplotlib import pyplot as plt  
plt.plot(input, sigmoid(input), c="r")
plt.show()
#print(input,sigmoid(input))