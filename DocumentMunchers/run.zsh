#!/bin/zsh
# source venv/bin/activate
# cd "./FrontEnd/" && npm run dev & python3 "./BackEnd/API/api.py"
python3 "./BackEnd/API/api.py" & cd "./FrontEnd/" && npm run dev