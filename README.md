
# iaav
Artistic Movement Recognition using Deep CNNs

Classify artwork into artistic styles

Pași:

1. Descărcăm setul de date Pandora18k (1.4 GB)

mkdir pandora

cd pandora/

wget http://imag.pub.ro/pandora/Download/Pandora_18k.zip

2. Dezarhivăm fișierul (18.730 poze, ~1k fișiere/clasă)

unzip Pandora_18k.zip

3. Arhiva este împărțită în 18 foldere corespunzătoare următoarelor curente artistice:
        - 01 byzantin iconography
        - 02 early renaissance
        - 03 northern renaissance
        - 04 high renaissance
        - 05 baroque
        - 06 rococo
        - 07 romanticism
        - 08 realism
        - 09 impressionism
        - 10 post impressionism
        - 11 expressionism
        - 12 symbolism
        - 13 fauvism
        - 14 cubism
        - 15 surrealism
        - 16 abstractart
        - 17 naiveart
        - 18 popart
        
    De asemenea, fiecare folder este împărțit pe autori; întrucât nu avem nevoie de această informație, vom muta toate picturile unui curent artistic într-un singur folder, respectiv în folderul părinte
    
for D in \*; do { \[ -d "${D}" ]; mv "${D}"/\*/* "${D}"/ ; rmdir "${D}"/* ; } done

3'. Obs: am redenumit manual picturile cu același nume de fișier pentru mai mulți artiști din cadrul aceluiași curent; ar trebui trecut numele artistului ca prefix în numele fișierului

4. Am folosit codul din acest tutorial: https://www.tensorflow.org/tutorials/image_retraining
    
    Descărcăm script-ul de retrain: acesta folosește niște rețele preantrenate
    și reantrenează ultimul strat conform noilor clase pe care le avem în setul nostru de date

curl -LO https://github.com/tensorflow/hub/raw/r0.1/examples/image_retraining/retrain.py

5. Reantrenarea
    - ResNet v2 50 (50 de straturi de convoluție), input de 224x224, 18 clase
    - întâi se creează niște fișiere bottleneck pentru fiecare poză, respectiv
      ce obține rețeaua după ce trece de straturile înghețate ale rețelei date ca parametru
    - după crearea acestor fișiere, începe (re)antrenarea propriu-zisă:
        - implicit, datele sunt împărțite astfel: 80% antrenare, 10% validare, 10% testare
        - la antrenare, se iau batch-uri de câte 10 imagini
        - implicit, sunt 4000 de iterații; am ales 2000 întrucât setul de date
          nu este atât de mare
    - la sfârșit se salvează fișierele de checkpoint și cele de log
    - script-ul împarte automat setul de date în train/validation/test, alegând
      imagini din fiecare clasă în mod aleator

source ~/tensorflow/bin/activate

python3 retrain.py --image_dir pandora/ --bottleneck_dir bottleneck/ --tfhub_module https://tfhub.dev/google/imagenet/resnet_v2_50/feature_vector/1 --summaries_dir summaries_dir/ --saved_model_dir saved_model_dir_2000/ --how_many_training_steps 2000

5'. Obs: O parte din fișiere se salvează în folderul /tmp/ așa că facem o copie

cp -r /tmp/tfhub_modules/ tfhub_modules

5'. Am obținut acuratețe 63% pe mulțimea de antrenare și 51% la validare

tensorboard --logdir=summaries_dir

6. Vom testa și cu alte imagini pentru a ne convinge că rețeaua nu face overfitting și că totuși am învățat ce trebuie
        - testăm cu picturi ai unor artiști care nu sunt în setul de date inițial

python download.py

Folosind script-ul menționat mai sus, am descărcat picturile de pe site-ul personal al artistului Dorel Topan; stilul său artistic este Pop art

Dorel Topan: http://www.doreltopan.com/lucrari.html

Camil Ressu: https://www.wikiart.org/en/camil-ressu -> impresionism

Simon Hollosy: https://www.muzartbm.ro/simon-hollosy/ -> mai multe stiluri

curl -LO https://github.com/tensorflow/tensorflow/raw/master/tensorflow/examples/label_image/label_image.py

imagine un pic modificată din setul inițial, pentru a testa că a învățat (și) asta

python label_image.py --graph=output_graph.pb --labels=output_labels.txt --input_layer=Placeholder --output_layer=final_result --input_height=224 --input_width=224 --image=test_images/Le-Cri-par-Edvard-Munch-haute-qualit-peintures-l-huile-reproduction.jpg_640x640.jpg

imagine puțin modificată, nu se regăsește în setul inițial; rezultatul nu este foarte surprinzător, întrucât rețeaua se poate ghida în acest caz după fundal

python label_image.py --graph=output_graph.pb --labels=output_labels.txt --input_layer=Placeholder --output_layer=final_result --input_height=224 --input_width=224 --image=test_images/scream_trumpet.jpg

Dorel Topan - popart

exemplu în care a greșit!

python3 label_image.py --graph=output_graph.pb --labels=output_labels.txt --input_layer=Placeholder --output_layer=final_result --input_height=224 --input_width=224 --image=test_images/topan/2010_3.jpg


Camil Ressu - impresionist

python3 label_image.py --graph=output_graph.pb --labels=output_labels.txt --input_layer=Placeholder --output_layer=final_result --input_height=224 --input_width=224 --image=test_images/ressu/after-work-1913.jpg

python3 label_image.py --graph=output_graph.pb --labels=output_labels.txt --input_layer=Placeholder --output_layer=final_result --input_height=224 --input_width=224 --image=test_images/ressu/elenbergen-1916.jpg

python3 label_image.py --graph=output_graph.pb --labels=output_labels.txt --input_layer=Placeholder --output_layer=final_result --input_height=224 --input_width=224 --image=test_images/ressu/peasant-funeral-1912.jpg

python3 label_image.py --graph=output_graph.pb --labels=output_labels.txt --input_layer=Placeholder --output_layer=final_result --input_height=224 --input_width=224 --image=test_images/ressu/two-sisters-1915.jpg

Simon Hollosy -> nu se încadrează într-un singur stil

post-impresionism + impresionism

python3 label_image.py --graph=output_graph.pb --labels=output_labels.txt --input_layer=Placeholder --output_layer=final_result --input_height=224 --input_width=224 --image=test_images/hollosy/03-cetatea-hustului_1896.jpg

romantism + realism

python3 label_image.py --graph=output_graph.pb --labels=output_labels.txt --input_layer=Placeholder --output_layer=final_result --input_height=224 --input_width=224 --image=test_images/hollosy/amurg.jpg

impresionism + realism

python3 label_image.py --graph=output_graph.pb --labels=output_labels.txt --input_layer=Placeholder --output_layer=final_result --input_height=224 --input_width=224 --image=test_images/hollosy/clai-de-fan.jpg

chef în cârciumă! realism + impresionism

python3 label_image.py --graph=output_graph.pb --labels=output_labels.txt --input_layer=Placeholder --output_layer=final_result --input_height=224 --input_width=224 --image=test_images/hollosy/chef-in-circiuma_1888.jpg

deși nu e pictură, stilul este corect!

python3 label_image.py --graph=output_graph.pb --labels=output_labels.txt --input_layer=Placeholder --output_layer=final_result --input_height=224 --input_width=224 --image=test_images/DSC_1245.JPG

nu este pictură: faptul că niciun stil nu este dominant înseamnă că și rețeaua își dă seama că nu este vorba despre picturi

python3 label_image.py --graph=output_graph.pb --labels=output_labels.txt --input_layer=Placeholder --output_layer=final_result --input_height=224 --input_width=224 --image=test_images/DSC_1348.JPG

exemplu "corect": justificarea este dată de faptul că în stilul bizantin predomină icoanele, prin extensie și cercurile

python3 label_image.py --graph=output_graph.pb --labels=output_labels.txt --input_layer=Placeholder --output_layer=final_result --input_height=224 --input_width=224 --image=test_images/DSC_1342.JPG

exemplu greșit

python3 label_image.py --graph=output_graph.pb --labels=output_labels.txt --input_layer=Placeholder --output_layer=final_result --input_height=224 --input_width=224 --image=test_images/Mastere\ noi\ informatica.jpg

exemplu cu mai multe stiluri; evident, nu este vorba despre o pictură, motiv pentru care nu avem niciuna dintre probabilități mari

python3 label_image.py --graph=output_graph.pb --labels=output_labels.txt --input_layer=Placeholder --output_layer=final_result --input_height=224 --input_width=224 --image=test_images/calc_risk.jpg 






DEPRECATED: The notebook can also be found [here](https://drive.google.com/file/d/1eGQ0Tz5P1nDymjstS3r21RAt2MHuavY1/view?usp=sharing) (see steps above instead).


## Introduction
Artistic movement recognition is a challenging image classification task. Unlike the ImageNet challenge, where the target is to recognize an object from a large number of classes, artistic style does not rely on object types, but on some more abstract features. For example, still life is a recurrent theme across multiple artistic movements.

Despite the fact that recognizing artistic style is not a new research topic, the usual approaches are based on traditional machine learning techniques, such as Naive Bayes and SVM. One limitation of this approach is the small number of classes, usually fewer than 13 classes. Another problem is the datasets used, with no more than 5.000 paintings.
## Related work
Deep learning approaches haven't been tried until recently due to lack of digitized artworks. [Karayev et al (2014)](https://sergeykarayev.com/files/1311.3715v3.pdf) used Flickr and [WikiPaintings](https://www.wikiart.org/) (it has around 80.000 paintings). They applied transfer learning on an eight-layer CNN pre-trained on ImageNet.

[Yu et al (2017)](http://cs231n.stanford.edu/reports/2017/pdfs/411.pdf) used Inception and VGG and fine-tuned the last convolutional layer and the last fully connected layers. They noted that WikiPaintings alone is not a great dataset because the number of paintings among movements vary a lot. Also, it is community based, with little help from experts and also contains other types of art, such as sculptures. They used the [Pandora18k](http://imag.pub.ro/pandora/pandora_download.html) dataset instead (a subset of WikiPaintings), with 18.038 paintings distributed almost evenly among 18 classes and manually revised by experts.
## Proposed architecture
Because of the little amount of labeled data available, deep neural networks cannot be used directly. The idea is to use transfer learning. We take a network pre-trained on a much larger dataset, such as ImageNet, in order to take advantage of the low-level features like edges which are common among these two classification tasks. Then, we re-train the last layer, because it encodes domain-specific features. Of course, because the ImageNet challenge has 1.000 classes, we need to replace the fully connected layer according to our needs: 18 classes corresponding to the movements we want to recognize.


## Results
Train: 63%

Validation: 51%

> Written with [StackEdit](https://stackedit.io/).
