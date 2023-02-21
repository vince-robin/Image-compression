
## Organisation du répertoire

* :file_folder: [/imgs](imgs) : images à tester que j'ai sélectionné pour leurs caractéristiques remarquables. Elles ont des textures/nuances différentes, présentent des faibles/fortes variations de couleurs, ont des dimensions différentes (divisibles ou non par la taille de bloc). Je mets également à disposition des images synthétiques simples .ppm générées avec mon script Python.

* :file_folder: [/vhdl](vhdl) : quelques briques VHDL du processus de compression/décompression (typiquement RLE, DCT, Zigzag) pour une future implémentation sur FPGA. Les codes utilisent un environnement logiciel très léger : ils sont compilables avec *GHDL* et simulables avec *GTKWave*.

* :file_folder: [/functions](functions) : des fonctions Python écrites pour mener à bien le projet (par exemple le script de génération d'images synthétiques, ...)


## Comment exécuter le code du compresseur ?

    python3 encoder.py -input img_to_compress.jpeg -quality 80 -huffman dynamic


Le programme attend les options suivantes :

- **input** : image d'entrée à compresser à placer dans le répertoire [/img](img). Le format est libre (.png, .jpg, .jpeg, .tiff, .bmp...) et l'image peut être de toutes les tailles possibles.
- **quality** : choix du niveau de quantification. Plus la valeur est grande, meilleure est la qualité de l'image compressée. En contrepartie, le taux de compression est moins important.
- **huffman** : sélection de la manière d'adresser les tables de Huffman au décodeur. En mode "dynamic" les tables sont différentes pour chaque images, il faut donc transmettre les dictionnaires des 3 canaux Y,Cr,Cb au décodeur. En mode "static" les tables de Huffman utilisées sont les mêmes pour toutes les images, ce sont celles du standard JPEG définies dans le fichier [tables.py](tables.py).

En sortie, le programme génère un flux de données binaires [bitstream.txt](bitstream.txt) issu du codage de Huffman, et en fonction du mode d'adressage des tables de Huffman, trois dictionnaires pour les canaux Y, Cr, Cb. 
Ce fichier possède en première ligne des ifnrmations supplémentaires que le décodeur doit connaitre :

- le niveau de quantification (le compresseur et le décompresseur doivent s'accorder sur la même valeur)
- les dimension de l'image d'origine (hauteur et largeur)

## Comment exécuter le code du décompresseur ?

    python3 decoder.py -input bitstream.txt -huffman dynamic


Le programme attend les options suivantes :

- **input** : le flux de données encodés [bitstream.txt](bitstream.txt)
- **huffman** : sélection de la manière de recevoir les tables de Huffman. En mode "dynamic" les dictionnaires de Huffman utilisées pour les 3 canaux Y,Cr,Cb sont ceux générés par le compresseur. En mode "static" les tables de Huffman utilisées pour la décompression sont celles du standard JPEG définies dans le fichier [tables.py](tables.py).

En sortie, le programme sauvegarde l'image décompressée au format .jpg


## Version et Packages de Python

- La version de Python utilisée pour le projet est la *3.8.6*
- Les packages à installer, si ce n'est pas déjà le cas, sont :
    - matplotlib : `pip install matplotlib`
    - numpy : `pip install numpy`
    - opencv : `pip install opencv-python`
