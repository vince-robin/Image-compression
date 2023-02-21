## Comment exécuter les codes VHDL ?

Je fournis dans chaque répertoire un script bash [compile.x](compile.x) qui automatise le processus d'analyse et d'élaboration avec *GHDL* et la visualisation des formes d'ondes avec *GTKWave*.
S'assurer au préalable que les droits d'exécution ont été accordés à l'utilisateur avant de lancer le script :

    $  chmod +x compile.x
    
    $  ./compile.x
    
 Les constantes, et les types utiles pour les différents fichiers VHDL sont présents dans le package VHDL [pkg.vhd](pkg.vhd)
 
 
## Comment installer GHDL et GTKWave sous Linux

    $   sudo apt-get install ghdl gtkwave


Pour les inconditionnels de Windows, GHDL et GTKWave peuvent être installées depuis WSL avec la même commande.


## Générations des testbenchs

La structure des testbenchs VHDL a été générée avec le formidable parser pour VHDL *Vertigo* écrit en Ruby par [Jean Christophe Le Lann](https://github.com/JC-LL/vertigo)

Pour l'installer puis générer un testbench utiliser les commandes :

    $  gem install vertigo_vhdl
    
    $  vertigo --gen_tb file_with_entity.vhd

