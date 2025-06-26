# experiments-autogen


## Pre-requesites :
Autogen needs Python >= 3.10.

Packages needed : autogen-agentchat autogen-ext[openai]

Optional :
* pip install autogen-agentchat[gemini]

API key needed : 
* Add a variable OPENAI_API_KEY in the environement. In bash or zsh (.bashrc or .zshrc) export OPENAI_API_KEY=...
* Optional : add a GEMINI_API_KEY.

## Configuration

### Command line
* python3.10 -m venv ~/BIN/pyt310 (for instance)
* source ~/BIN/pyt310/bin/activate
* python -V
* pip install -U "autogen-agentchat" "autogen-ext[openai]"

### PyCharm
* There is a menu in the bottom-right part of the window to choose a venv for the project.
* From that menu you can also install package (like pip install)

### Notebook
When using a notebook instead of a python script:
* Use python-dotenv to import de environment variable from a .env file
* use await main() instead of asyncio.run(main())
