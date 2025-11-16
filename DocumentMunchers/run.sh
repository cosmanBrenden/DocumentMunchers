#!/bin/bash
source venv/bin/activate
python3 "./BackEnd/API/api.py" & cd "./FrontEnd/" && npm run dev