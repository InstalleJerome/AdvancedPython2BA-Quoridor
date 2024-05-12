# AdvancedPython2BA-Quoridor
Bibliothèques nécessaires : socket et json

Stratégie : On bloque l'adversaire s'il est plus proche de la fin du plateau. Lorsqu'on est bloqué, on regarde à droite et à gauche 
quelle est la case libre la plus proche pour voir dans quelle direction on va (la stratégie est pareille si on est bloqué également à gauche et à droite).