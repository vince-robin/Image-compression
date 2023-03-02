
## Organisation du répertoire

* :file_folder: [/codes_wiki](codes_wiki) : les codes utilisés dans les différentes parties du Wiki

* :file_folder: [/functions](functions) : des fonctions Python écrites pour mener à bien le projet (par exemple le script de génération d'images synthétiques, ...)

* :file_folder: [/imgs](imgs) : images à tester que j'ai sélectionné pour leurs caractéristiques remarquables. Elles ont des textures/nuances différentes, présentent des faibles/fortes variations de couleurs, ont des dimensions différentes (divisibles ou non par la taille de bloc). Je mets également à disposition des images synthétiques simples .ppm générées avec mon script Python.

* :file_folder: [/jupyter_notebook](jupyter_notebook) : une démonstration de l'algorithme sous sa première version dans un Jupyter Notebbok (contient des erreurs)

* :file_folder: [/vhdl](vhdl) : quelques briques VHDL du processus de compression/décompression (typiquement RLE, DCT, Zigzag) pour une future implémentation sur FPGA. Les codes utilisent un environnement logiciel très léger : ils sont compilables avec *GHDL* et simulables avec *GTKWave*.


## Comment exécuter le code du compresseur ?

    python3 -B compression.py img_to_compress.jpg -q 80    # "-B" option to ignore the generation of bytecode in the __pycache__ folder

Le programme attend les options suivantes :

- **input** : image d'entrée à compresser à placer dans le répertoire [/imgs](imgs). Le format est libre (.png, .jpg, .jpeg, .tiff, .bmp...) et l'image peut être de toutes les tailles possibles.
- **quality** (optionnelle, valeur par défaut = 50) : choix du niveau de quantification. Plus la valeur est grande, meilleure est la qualité de l'image compressée. En contrepartie, le taux de compression est moins important. 


En sortie, le programme génère dans le répertoire [/outputs](outputs) un flux de données binaires [compressed_data.bin](https://github.com/vince-robin/Image-compression/edit/main/soft/outputs/compressed_data.bin) et les tables de Huffman (au format .json) pour les trois composantes Y, Cr, Cb. Une série d'analyses graphiques est générée dans le répertoire [/analyse](analyse). 
Le fichier binaire possède un en-tête, introduit avant les données compressées, et contenant des informations que le décodeur doit connaitre :

- le niveau de quantification (le compresseur et le décompresseur doivent s'accorder sur la même valeur),
- les dimensions de l'image d'origine (hauteur et largeur),
- les dimensions des composantes de luminance et de chrominance (Cr et Cb).

Voici ce que le programme doit afficher à l'utilisateur dans le terminal :

    Original picture dimension: (436 x 500)
    Total number of bits:  5232000
    Zero padding: is required
    Quantization level is (1-99):  40

    Files correctly generated:
      --> cbHuffman_dict.json
      --> compressed_data.bin
      --> crHuffman_dict.json
      --> yHuffman_dict.json

    Number of bits after compression:  69837
    Compression rate:  74.92
    Execution time:  1.06sec

    Huffman analysis:
    --------------------------------------------------------------------------------------------------------------------------------------
                 Luminance Y                |               Chrominance Cr                  |               Chrominance Cb
    --------------------------------------------------------------------------------------------------------------------------------------
    Symbol          Proba   Code    Length  |       Symbol          Proba   Code    Length  |       Symbol          Proba  Code     Length
    --------------------------------------------------------------------------------------------------------------------------------------
    (1, 0)          0.146   100     3       |       (-1, 0)         0.121   010     3       |       (-1, 0)         0.108  100      3
    (-1, 0)         0.137   110     3       |       (1, 0)          0.086   1111    4       |       (1, 0)          0.092  1111     4
    (-1, 1)         0.05    0001    4       |       (47, 7)         0.054   00110   5       |       (1, 1)          0.041  0011     5
    (2, 0)          0.048   0100    4       |       (2, 0)          0.041   01101   5       |       (50, 7)         0.039  11001    5
    (-2, 0)         0.047   0011    4       |       (48, 7)         0.041   11011   5       |       (2, 0)          0.036  10101    5
    (1, 1)          0.044   11111   5       |       (-2, 0)         0.036   11000   5       |       (51, 7)         0.032  10111    5
    (3, 0)          0.022   00000   5       |       (1, 1)          0.035   11010   5       |       (-1, 1)         0.028  11011    5
    (-3, 0)         0.022   010111  6       |       (-1, 1)         0.033   10101   5       |       (-2, 0)         0.026  11100    5
    (-1, 2)         0.018   111100  6       |       (45, 7)         0.016   00010   5       |       (55, 7)         0.024  001001   5
    (1, 2)          0.017   101011  6       |       (46, 7)         0.015   00011   5       |       (52, 7)         0.024  010001   5
    --------------------------------------------------------------------------------------------------------------------------------------
    Total           0.549                   |       Total           0.479                   |       Total           0.450
    --------------------------------------------------------------------------------------------------------------------------------------
    Entropy                         6.3     |       Entropy                         6.0     |       Entropy                6.1
    --------------------------------------------------------------------------------------------------------------------------------------


## Comment exécuter le code du décompresseur ?

    python3 -B decompression.py     # "-B" option to ignore the generation of bytecode in the __pycache__ folder


En sortie, le programme sauvegarde dans le répertoire [/outputs](outputs) l'image décompressée au format .jpg et .ppm ainsi qu'une série d'analyses sous forme graphique dans le répertoire [/analyse](analyse).

Voici ce que le programme doit afficher à l'utilisateur dans le terminal :

    Original picture dimensions: 436x500
    Quantization level (1-99): 40
    Execution time: 5.15 sec
    SNR: 26.57 dB
    MSE: 227.39
 
 Voici le schéma de principe de processus de compression et de décompression utilisant les scripts Python : 
<img src = "https://github.com/vince-robin/Image-compression/blob/main/imgs/compression_decompression_demonstration.png" width=700>

## Version et Packages de Python

- La version de Python utilisée pour le projet est la *3.8.6*
- Les principaux packages à installer, si ce n'est pas déjà le cas, sont :
    - matplotlib : `pip install matplotlib`
    - numpy : `pip install numpy`
    - opencv : `pip install opencv-python`
