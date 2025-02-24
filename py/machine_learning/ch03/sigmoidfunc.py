import numpy as np
import matplotlib.pyplot as plt


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


x = np.arange(-10.0, 10.0, 0.1)
y = sigmoid(x)
print(x)
print(y)

plt.plot(x, y)
plt.ylim(-0.1, 1.1)
plt.show()
