# CS:GO Cheats Exploration Project
This projects aim is to replicate common cheats in CS:GO in python, as it is easier to understand than lower level languages such as c or c++.

## Disclaimer
This project is solely intended for educational purposes. The purpose of this repository is to explore and better understand how cheats operate within the context of the Counter-Strike: Global Offensive (CS:GO) game. The cheats developed here are not meant to be used in any malicious or competitive manner. The creators of this project do not endorse or encourage cheating in any form.

## About
This Project is aiming to grant insight in how direct memory access works and how much can be done with it. 

## Must do before being able to use
in pymem\.process replace:
``` python
        yield module_info
```
with:
``` python
        yield [module_info, hModule]
```