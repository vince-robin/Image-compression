## Conception d'un modèle de référence pour la compression d'images

##### Vincent Robin, étudiant à l'ENSTA Bretagne (grande école d'ingénieurs pour l'innovation dans le secteur maritime, la défense et les entreprises de haute technologie)

##### Sous la direction de [Jean-Christophe Le Lann](https://github.com/JC-LL) et [Pascal Cotret](https://github.com/pcotret/) , enseignants-chercheurs à l'ENSTA Bretagne 

## Introduction 

La compression d'images est un domaine emblématique des systèmes multimédia. L’élaboration de normes de compression efficaces revêt une importance cruciale notamment du fait de l’explosion de la consommation de vidéo sur internet, consommatrice de bande passante.
Le projet vise en premier lieu à élaborer un modèle de référence (inspiré de la norme JPEG) capable de compresser une image. Le but final est de travailler dans un contexte dynamique, sur une vidéo et d'implémenter l'algorithme sur une cible FPGA (qui pourra par exemple capter une séquence vidéo avec une caméra bon marché du type [OV7670](https://www.eagle-robotics.com/cameras/78-camera-ov7670-compatible-arduino-0780201370781.html) 


## Organisation du répertoire

* :file_folder: [/doc](doc) : documentations, présentations, articles scientifiques, et datasheets consultés pour la réalisation de ce projet. Je conseille en particulier de consulter la notice du [standard JPEG](/doc/Jpeg_Standard_ITU_RecommendationT81_approved_by_CCITT) sur laquelle je me suis inspirée pour la construction de mon modèle. 
* :file_folder: [/soft](soft) : contient tout les développements, des fonctions utiles, et en particulier, les programmes Python de l'[encodeur](/soft/encoder.py) qui compresse une image du [décodeur](/soft/decoder.py) et qui la décompresse. Je fournis également quelques briques VHDL (DCT, RLE, Zigzag scanning) pour une future implémentation sur FPGA.


## Informations supplémentaires

Malgré tous mes efforts, et l'attention portée à mes développements, je n'apporte aucune garantie de qualité ou d'adéquation à un usage particulier. Ce projet est le fruit de mes propres développements, c'est pourquoi, j'exige, à minima, un pointeur vers mon git en cas de réutilisation de tout ou partie de mes codes. 
