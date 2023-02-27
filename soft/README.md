
## Organisation du répertoire

* :file_folder: [/imgs](imgs) : images à tester que j'ai sélectionné pour leurs caractéristiques remarquables. Elles ont des textures/nuances différentes, présentent des faibles/fortes variations de couleurs, ont des dimensions différentes (divisibles ou non par la taille de bloc). Je mets également à disposition des images synthétiques simples .ppm générées avec mon script Python.

* :file_folder: [/vhdl](vhdl) : quelques briques VHDL du processus de compression/décompression (typiquement RLE, DCT, Zigzag) pour une future implémentation sur FPGA. Les codes utilisent un environnement logiciel très léger : ils sont compilables avec *GHDL* et simulables avec *GTKWave*.

* :file_folder: [/functions](functions) : des fonctions Python écrites pour mener à bien le projet (par exemple le script de génération d'images synthétiques, ...)


## Comment exécuter le code du compresseur ?

    python3 -B compression.py img_to_compress.jpg -q 80


Le programme attend les options suivantes :

- **input** : image d'entrée à compresser à placer dans le répertoire [/imgs](imgs). Le format est libre (.png, .jpg, .jpeg, .tiff, .bmp...) et l'image peut être de toutes les tailles possibles.
- **quality** (optionnel, valeur par défaut 50) : choix du niveau de quantification. Plus la valeur est grande, meilleure est la qualité de l'image compressée. En contrepartie, le taux de compression est moins important. 

En sortie, le programme génère dans le répertoire [/outputs](outputs) un flux de données binaires [compressed_data.bin](https://github.com/vince-robin/Image-compression/edit/main/soft/outputs/compressed_data.bin) et les tables de Huffman (au format .json) pour les trois composantes Y, Cr, Cb. Une série d'analyses graphique est générée dans le répertoire [/analyse](analyse). 
Le fichier binaire possède un en-tête, introduit avant les données compressées, et contenant des informations que le décodeur doit connaitre :

- le niveau de quantification (le compresseur et le décompresseur doivent s'accorder sur la même valeur)
- les dimension de l'image d'origine (hauteur et largeur)
- les dimensions des composantes de luminance et de chrominance (Cr et Cb)

## Comment exécuter le code du décompresseur ?

    python3 -B decompression.py


En sortie, le programme sauvegarde dans le répertoire [/outputs](outputs) l'image décompressée au format .jpg et .ppm ainsi qu'une série d'analyses sous forme graphique dans le répertoire [/analyse](analyse).


## Version et Packages de Python

- La version de Python utilisée pour le projet est la *3.8.6*
- Les principaux packages à installer, si ce n'est pas déjà le cas, sont :
    - matplotlib : `pip install matplotlib`
    - numpy : `pip install numpy`
    - opencv : `pip install opencv-python`
