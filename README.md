
# iaav
Artistic Movement Recognition using Deep CNNs

Classify artwork into artistic styles

The notebook can also be found [here](https://drive.google.com/file/d/1eGQ0Tz5P1nDymjstS3r21RAt2MHuavY1/view?usp=sharing).


## Introduction
Artistic movement recognition is a challenging image classification task. Unlike the ImageNet challenge, where the target is to recognize an object from a large number of classes, artistic style does not rely on object types, but on some more abstract features. For example, still life is a recurrent theme across multiple artistic movements.

Despite the fact that recognizing artistic style is not a new research topic, the usual approaches are based on traditional machine learning techniques, such as Naive Bayes and SVM. One limitation of this approach is the small number of classes, usually fewer than 13 classes. Another problem is the datasets used, with no more than 5.000 paintings.
## Related work
Deep learning approaches haven't been tried until recently due to lack of digitized artworks. [Karayev et al (2014)](https://sergeykarayev.com/files/1311.3715v3.pdf) used Flickr and [WikiPaintings](https://www.wikiart.org/) (it has around 80.000 paintings). They applied transfer learning on an eight-layer CNN pre-trained on ImageNet.

[Yu et al (2017)](http://cs231n.stanford.edu/reports/2017/pdfs/411.pdf) used Inception and VGG and fine-tuned the last convolutional layer and the last fully connected layers. They noted that WikiPaintings alone is not a great dataset because the number of paintings among movements vary a lot. Also, it is community based, with little help from experts and also contains other types of art, such as sculptures. They used the [Pandora18k](http://imag.pub.ro/pandora/pandora_download.html) dataset instead (a subset of WikiPaintings), with 18.038 paintings distributed almost evenly among 18 classes and manually revised by experts.
## Proposed architecture
Because of the little amount of labeled data available, deep neural networks cannot be used directly. The idea is to use transfer learning. We take a network pre-trained on a much larger dataset, such as ImageNet, in order to take advantage of the low-level features like edges which are common among these two classification tasks. Then, we re-train some of the last convolutional layers, those who encode domain-specific features. Of course, because the ImageNet challenge has 1.000 classes, we also need to replace the fully connected layers according to our needs: 25 classes corresponding to the movements we want to recognize.

We chose the architecture described in [
Lecoutre et al (2017)](http://www.lamsade.dauphine.fr/~bnegrevergne/webpage/documents/2017_rasta.pdf), which is ResNet50 trained on ImageNet. The advantage of using a residual network is its' ability to learn something new on top of something already learnt. Another benefit is that we can train more layers, resulting in more fine-grained features. This is possible because we preserve the signal through the network using shortcut connections and identity blocks, avoiding the problem of vanishing gradients.

![ResNet50](https://lh4.googleusercontent.com/srBJZGyRjz4WfhVmfcE0ktf_Z91-wV0SarCnqXoaC3sKa3C4MOopDI3Lwjj6sSBV3Dbtr1uP7-qKxg=w1920-h974-rw)

B represents a bottleneck block (shown in detail below).

![Bottleneck block](https://cdn-images-1.medium.com/max/1600/1*blFlm-UTF2N6gQTmhRPfkA.png)

## Results
According to the experiments in Lecoutre et al (2017), residual networks achieve the best results. We used the WikiPaintings-test dataset provided by Lecoutre et al (2017). With only the last FC retrained, we obtain the following results:

|  Top-1| Top-3 | Top-5 |
|-------|-------|-------|
| 0.494 | 0.771 | 0.874 |

Retraining ~20% of the top layers, the results are much better:

|  Top-1| Top-3 | Top-5 |
|-------|-------|-------|
| 0.615 | 0.851 | 0.931 |

## Conclusions, future work
Analyzing the confusion matrix in the linked articles, we can conclude that, most of the time, the network outputs the wrong answer on very similar classes, such as Renaissance and Late Renaissance, where humans also tend to disagree.

Therefore, having a top-5 accuracy of >90% is impressive and shows potential for further deep learning approaches.

Future work would include using the more carefully analyzed Pandora18k dataset and other novel deep architectures, with smaller convolutions (this one starts with a 7x7 conv). Transfer learning remains the starting point for this task.

> Written with [StackEdit](https://stackedit.io/).
