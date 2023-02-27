# Conception d'un modèle de référence pour la compression d'images

*Vincent Robin, étudiant à l'ENSTA Bretagne (grande école d'ingénieurs pour l'innovation dans le secteur maritime, la défense et les entreprises de haute technologie)*

*Sous la direction de [Jean-Christophe Le Lann](https://github.com/JC-LL) et [Pascal Cotret](https://github.com/pcotret/) , enseignants-chercheurs à l'ENSTA Bretagne*


## Introduction 

La compression d'images est un domaine emblématique des systèmes multimédias. L’élaboration de normes de compression efficaces revêt une importance cruciale notamment du fait de l’explosion de la consommation de vidéo sur internet, consommatrice de bande passante.
Le projet vise en premier lieu à élaborer un modèle de référence (inspiré de la norme JPEG) capable de compresser une image. Le but final est de travailler dans un contexte dynamique, sur une vidéo et d'implémenter l'algorithme sur une cible FPGA (qui pourra par exemple capter une séquence vidéo avec une caméra bon marché du type [OV7670](https://www.eagle-robotics.com/cameras/78-camera-ov7670-compatible-arduino-0780201370781.html)).


## Structure du modèle de référence

L'algorithme de compression/décompression reprend en grande partie les étapes connues du standard JPEG, à savoir :
- conversion de l'espace des couleurs (RGB vers YUV),
- sous-échantillonnage de la chrominance (4:4:4 vers 4:4:2 ou 4:2:0),
- découpage en blocs 8x8 de 64 pixels,
- zero-padding (uniquement pour les images de dimensions non divisibles par la taille de bloc),
- DCT (*Discrete Cosine Transform*),
- quantification des blocs de pixels,
- Zigzag,
- RLE (*Run-Length Encoding*),
- codage entropique à longueur variable (Huffman).

<img src="/imgs/jpeg_process.jpg" alt="drawing" style="width:1000px;"/>

Le programme de décompression, reproduit à l'identique, mais dans l'ordre inverse, le processus de compression. 

Le modèle prend en entrée une image (le format est libre : .jpg/.jpeg, .png, .bmp, .tiff..., la dimension également), et je fournis aussi un script Python permettant de générer des images synthétiques au format PPM, images simples qui peuvent être utilisées pour tester les différentes phases de l'algorithme.

Le **compresseur** génère un fichier binaire *.bin* qui contient le flux de données (bitstream) encodé et trois dictionnaires de Huffman (au format JSON) utilisés pour le codage des canaux Y,Cr,Cb. Il affiche à titre d'informations le taux de compression (en prenant soin de prendre en compte la taille des dictionnaires de Huffman transmis au décodeur).

Le **décompresseur** utilise le train binaire et les dictionnaires de Huffman afin de reconstruire l'image d'origine qui est sauvegardé au format .jpg et au format .ppm


## Organisation du répertoire

* :file_folder: [/doc](doc) : documentations, présentations, articles scientifiques, et datasheets utilisés pour la réalisation de ce projet. Je conseille en particulier de consulter la notice du [standard JPEG](/doc/jpeg_standard/ITU_RecommendationT81_approved_by_CCITT.pdf) sur laquelle je me suis inspiré pour la construction de mon modèle. 
* :file_folder: [/soft](soft) : contient tout les développements, des fonctions utiles, et en particulier, les programmes Python de l'[encodeur](/soft/encoder.py) qui compresse une image du [décodeur](/soft/decoder.py) et qui la décompresse. Je fournis également quelques briques VHDL (DCT, RLE, Zigzag scanning) pour une future implémentation sur FPGA.


## Informations supplémentaires 

Un Wiki complet et structuré décrit explicitement chaque étape de l'algorithme de compression et de décompression. Je conseille également de prendre connaissance des README que j'ai ajouté dans les différents répertoires du projet.

## Avertissements

Malgré tous mes efforts, et l'attention portée à mes développements, je n'apporte aucune garantie de qualité ou d'adéquation à un usage particulier. Ce projet est le fruit de mes propres développements, c'est pourquoi, j'exige, à minima, un pointeur vers mon git en cas de réutilisation de tout ou partie de mes codes et/ou images. 
