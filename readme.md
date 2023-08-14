# CS:GO Cheats Exploration Project
This projects aim is to replicate common cheats in CS:GO in python, as it is easier to understand than lower level languages such as c or c++.

## Disclaimer
This project is solely intended for educational purposes. The purpose of this repository is to explore and better understand how cheats operate within the context of the Counter-Strike: Global Offensive (CS:GO) game. The cheats developed here are not meant to be used in any malicious or competitive manner. The creators of this project do not endorse or encourage cheating in any form.

## About
This Project is aiming to grant insight in how direct memory access works and how much can be done with it. 

## Must do before being able to use
### Install Packages
To install the required packages run the following command in your python 3.7 venv
``` bash
pip install -r requirements.txt
```
### Replace a line of code in pymem\.process
old:
``` python
yield module_info
```
new:
``` python
yield [module_info, hModule]
```
### Update the offsets
CS:GO offsets change with every update, so you need to get the new offsets from [Hazedumper](https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json).