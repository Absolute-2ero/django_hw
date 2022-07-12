# README
Use this word reviewer to randomly generate word lists and memorize words by yourself before exams!
The words will be selected from the given lexicon `./words/TPO_Reviewer.txt`.
To start this project, just type
```python
py build.py
```
in your command line and the program will generate 50 translated wordlists for you, with 15 words in each list.
If you want to change the parameters, please get into build.py to change them.
The meanings of these parameters are:
```python
1. -s: The size of each wordlist.
2. -r: Whether you want to choose these words randomly(Don't type "-r" if you don't want to select them randomly).
3. -lb: The lower bound of the label of the whole lexicon.
4. -rb: The upper bound of the label of the whole lexicon.
5. -t: Whether you want the selected words to be translated(Don't type "-t" if you don't want them to be translated).
6. -n: The number of wordlists you want to generate.
```
The wordlists will be stored in `./generated`.
## Environment Requirements
Basic requirements are written in `requirements.yaml.` Run `conda env create -n <env_name> -f ./requirements.yaml` to add a new environment to your conda.
This projects uses pygtrans pack, which is already included in requirements.yaml.
