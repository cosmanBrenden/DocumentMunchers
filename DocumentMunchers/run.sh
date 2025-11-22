#!/bin/bash
source venv/bin/activate
cd "./FrontEnd/" && npm run dev & python3 "./BackEnd/API/api.py"