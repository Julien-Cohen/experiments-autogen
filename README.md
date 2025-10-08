# Experiments with BDI concepts on AutoGen

This project explores the use of BDI concepts (Beliefs, Desires, Intentions) in AutoGen agents. 

We provide a `BDIRoutedAgent` class that extends the AutoGen `RoutedAgent` and embedds a BDI loop (directory `bdi_autogen`).
See its use in various classes in the use-case example (directory `example`).

## Pre-requesites :
Autogen needs Python >= 3.10.

Packages needed : `autogen-agentchat` `autogen-ext[openai]`


An API key is needed to run the examples : 
* Add a variable `OPENAI_API_KEY` in the environment. In bash or zsh (files `.bashrc` or .`zshrc`):
  * `export OPENAI_API_KEY=...`
* Alternatively : store your keys in a `.env` file containing `OPENAI_API_KEY=...` (use your own key but don't share it). You need the 
`python-dotenv` package installed. 

## Configuration

### Command line
* `python3.10 -m venv ~/BIN/pyt310` (for instance)
* `source ~/BIN/pyt310/bin/activate`
* `python -V`
* `pip install -U "autogen-agentchat" "autogen-ext[openai]"`
* or `pip install -r requirements.txt`
 
## Licence

Eclipse Public License - v 2.0

THE ACCOMPANYING PROGRAM IS PROVIDED UNDER THE TERMS OF THIS ECLIPSE PUBLIC LICENSE (“AGREEMENT”). ANY USE, REPRODUCTION OR DISTRIBUTION OF THE PROGRAM CONSTITUTES RECIPIENT'S ACCEPTANCE OF THIS AGREEMENT. 
