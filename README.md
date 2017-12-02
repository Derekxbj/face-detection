# face-detection

### Prerequisites
You need to install the Anaconda at first. You can select the "64-Bit Graphical Installer".

```
https://www.anaconda.com/download/#macos
```

### Packages installing
For running the code, we need to install some packages.

This is the package for the opencv which is a computer vision package.
```
conda install -c conda-forge opencv 
```
This is a useful package which have a series of OpenCV convenience functions.
```
pip install imutils 
```
The Keras deep learning framework.
```
conda install -c conda-forge keras
```

### Running the tests
After installing all the prerequisite packages, you can run the code now. To run the code, you need to enter following at command line:
```
python detect_smile.py --cascade haarcascade_frontalface_default.xml --model output/lenet.hdf5 
```
If running detect_smile_simple.py, you can just simply enter:
```
python -i detect_smile_simple.py
```
and enter:
```
count = detect_smile()
```
It will return the number of frame with label of "Smiling".
