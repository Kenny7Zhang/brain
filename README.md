# Brain
## Introduction
In our project, we intend to detect the Inner Cortical Surface and Pial Surface in Magnetic Resonance Image (MRI) of a brain. Inner Cortical Surface is a tessellation based in the cleaned and corrected inner cortical boundary mask; meanwhile, Pial Surface depends on Inner Cortical Surface and the tissue fraction of Grey Matter, White Matter and CSF in the brain. The generation for those two tessellations contributes to the Brain Registration, which is generally used in the biomedical and usually need a long-time computing by previous work. We use two methods to solve the problem. One is 3D patches classification and the other is 2D image edge detection. The first one do not have good result and the second one performs well.

## Methods
We tried two methods to detect surface of brain in MRI. Our training data are 3D brain models. The first method is to cut 3D models into patches and the second method is to cut 3D models into 2D images slice by slice.

### 1. 3D patch
We cut 3D models into patches. And the corresponding label is the central label of the patch. The architecture of this model is simple. 

1) input layer

2) flatten layer

3) full connected layer

4) output layer

In input layer, we input batch of 3D patches. Then in flatten layer we flat the 3D matrix into 1D vector. In full connected layer we increase the dimension of 1D vector. The size of our output layer is 2. The output is one-hot vector of size 2.
### 2. Slice by slice
We cut 3D models into 2D images slice by slice, which means we transfer the problem into finding edge of objects in 2D images. We use Holistically-Nested Edge Detection method[[1]](https://arxiv.org/pdf/1504.06375.pdf).

The architecture of the model is as follows:

<img src="images/3.jpeg" width="200" height="200">
<img src="images/4.jpeg" width="200" height="200">


The architectures contains five convolutional layers and each is followed by a side output layer. We concatenate the five side output layers and make another 1-filter convolutional layer, the output is our predicted image. We will set a threshold to determine whether a pixel in the image is edge or not. Then we calculate the loss between our predicted image and ground-truth image. For our MRI image, the distribution of edge and non-edge is extremely biased. About 90% of the label is 0 and only 10% is 1. So, we use class-balanced cross-entropy as our loss function instead of general cross-entropy.

## Experiments

### Dataset
Our dataset is generated from BrainSuite, a collection of open source software tools that enable largely automated processing of MRI of human brain. Each brain has two files. One is 3D matrix of the brain vertices and the other is a list of vertices belonging to edge.

A slice of the 3D matrix is like:

```
array([[0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 0],
       ..., 
       [0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 0]], dtype=int16)
```
It is an image like:

<img src="images/1.jpeg" width="200" height="200">

The corresponding label is like:

```
[[  41.30926514  117.4752655    24.88306046]
 [  42.18822098  117.37171936   25.00785828]
 [  42.77109909  117.3330307    25.24357986]
 ..., 
 [  79.03147888   90.86765289  149.97180176]
 [  79.74328613   90.50224304  149.8828125 ]
 [  79.18741608   91.3355484   149.72851562]]
```
We convert it to 3D matrix and visulize it like:

<img src="images/2.jpeg" width="200" height="200">

These two 3D matrix are the input and output of our network.

### Training

We use seven brains for training and one brain for testing. The batch size is set as 20 and the number of epoch is 200. We train our model in GPU for 2-3 hours.

### Evaluation
We compare all the output labels with the ground-truth labels and calculate precision, recall and fscore as our evaluation metrics.

## Results

### 1. Baseline
We define our baseline model as a model that classifies all label into 1. It has a precision of 0.03, recall of 1 and fscore of 0.058.

### 2. 3D patch
The result of this model is bad. The performance is the same as baseline model. It means the model can not learn any feature of a patch to determine whether it is edge or not. We tried using 3D convolutional layer instead of cutting input data into patches. The result is not changed. We think it is likely because the size of each patch is too small to learn the features. So we increase the kernel size of filters of 3D convolutional layer, but the time and memory consumption are both high. It turns out to be a bad model.
### 3. Slice by slice
Using our model, we detect the surface of one brain for testing. 

We visualized our result.

This is the original image:

<img src="images/5.jpeg" width="200" height="200">

This is the ground-true label:

<img src="images/6.jpeg" width="200" height="200">

We have a hyperparameter threshold and we do not know which value it should be. So we run our model under different thresholds from 0 to 1 with the interval of 0.05. Here is all the output images.

<img src="images/8.png" width="800" height="600">

We calculate the evaluation metrics of ouput under different thresholds. And we can see that when threshold is set as 0.85, the fscore is maximum. When threshold is set as 0.95, the precision is maximum. When threshold is set as 0.0, the recall is maximum.

<img src="images/9.jpeg" width="600" height="300">

<img src="images/10.jpeg" width="600" height="300">

<img src="images/11.jpeg" width="600" height="300">

We can compare the output images of maximum fscore, precision and recall.

<img src="images/12.jpeg" width="600" height="600">

We choose the maximum fscore image as our output. So the shreshold of our model is 0.85. We compare the metrics between baseline and our model as follows.

<img src="images/13.png" width="600" height="300">

## Reference
[1] Xie, S. and Tu, Z., 2015. Holistically-nested edge detection. In Proceedings of the IEEE international conference on computer vision (pp. 1395-1403).