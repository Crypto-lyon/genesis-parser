# genesis-parser

## Ce que fait le script

Il parse (lit) le genesis block de la block chain produite par le noeud insacoin, avec des indications de chaque action de manière à comprendre le procédé de lecture des données du bloc sérialisées. Il l'affiche ensuite, d'une manière dont l'ésthétique peut paraître douteuse mais dont l'efficacité est indéniable.  

## Comment l'utiliser

```
python3 parser.py <blk.dat file>
```
Si vous lui donnez un mauvais fichier et qu'il ne trouve pas les magic bytes, boucle infinie :D  

## Pourquoi ?

Ecrit juste avant un workshop à l'INSA, ce script est à but éducationnel et permet de comprendre ce qu'est vraiment une blockchain, de comprendre comment sont sérialisées les données, où elles sont stockées, et comment.  
[Lien vers l'évènement](https://www.meetup.com/Crypto-Lyon/events/256267578/).  
