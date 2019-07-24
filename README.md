# Bilge Blob Creator
This simple function creates random blobs or to put it in another way randomly curved closed loops.

Bilge Blob Creator was written with Python3 but can be easily converted to Python2.

### Detailed explanation:
Bilge picks random points in a specific circular range then interpolates them to
create a curve. For 0 and 2pi the random points are the same thus a closed loop is created.
The frequency and the amplitude of the blobs can be controlled with parameters.
Also blobs have white color inside and black color outside, if asked I can add a color parameter.
These blobs are originally created as masks this is why the colors are the way they are.

### Requirements:
```
SciPy >= 1.0.0

NumPy >= 1.14.0

matplotlib >= 2.1.2 (Optional: For viewing the blob)

(It probably also work with older versions, I did not check it.)
```

(I used these versions but most of lower versions should work)

### Conclusion:
Frames are created with a vectorized implementation so it is fast but if you want
to create multiple frames you have to use a loop in this implementation but for multiple
frames an implementation without loops can be created, I aim to do that but you are 
welcome to do that you just need to change the code so that frames are not
(height, height) matrices but (number_of_blobs, height, height) tensors.
