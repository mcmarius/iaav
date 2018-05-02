# iaav
Artistic Movement Recognition using Deep CNNs

Classify artwork into artistic styles

The notebook can also be found [here](https://drive.google.com/file/d/1eGQ0Tz5P1nDymjstS3r21RAt2MHuavY1/view?usp=sharing).


## Introduction
Artistic movement recognition is a challenging image classification task. Unlike the ImageNet challenge, where the target is to recognize an object from a large number of classes, artistic style does not rely on object types, but on some more abstract features. For example, still life is a recurrent theme across multiple artistic movements.

Despite the fact that recognizing artistic style is not a new research topic, the usual approaches are based on traditional machine learning techniques, such as Naive Bayes and SVM. One limitation of this approach is the small number of classes, usually fewer than 13 classes. Another problem is the datasets used, with no more than 5.000 paintings.
## Related work
Deep learning approaches haven't been tried until recently due to lack of digitized artworks. [Karayev et al (2014)](https://sergeykarayev.com/files/1311.3715v3.pdf) used Flickr and [WikiPaintings](https://www.wikiart.org/) (also called WikiArt; it has around 80.000 paintings). They applied transfer learning on an eight-layer CNN pre-trained on ImageNet.

[Yu et al (2017)](http://cs231n.stanford.edu/reports/2017/pdfs/411.pdf) used Inception and VGG and fine-tuned the last convolutional layer and the last fully connected layers. They noted that WikiPaintings alone is not a great dataset because the number of paintings among movements vary a lot. Also, it is community based, with little help from experts and also contains other types of art, such as sculptures. They used the [Pandora18k](http://imag.pub.ro/pandora/pandora_download.html) dataset instead (a subset of WikiPaintings), with 18.038 paintings distributed almost evenly among 18 classes and manually revised by experts.
## Proposed architecture
Because of the little amount of labeled data available, deep neural networks cannot be used directly. The idea is to use transfer learning: we take a network pre-trained on a much larger dataset, such as ImageNet, in order to take advantage of the low-level features like edges which are common among these two classification tasks.
## Results

## Conclusions, future work


> Written with [StackEdit](https://stackedit.io/).
