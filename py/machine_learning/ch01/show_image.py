# show an image test

import matplotlib.pyplot as plt
from matplotlib.image import imread

img = imread('../images/angry_cat.jpg')
plt.imshow(img)

plt.show()
