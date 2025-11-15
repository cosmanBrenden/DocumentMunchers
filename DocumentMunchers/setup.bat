@echo off

cd FrontEnd
npm i
cd ..

python -m venv venv
call venv\Scripts\activate.bat
pip install flask
pip install flask_cors
pip install transformers
pip install sentence_transformers
pip install pdfminer
pip install pdfminer.six
pip install PyPDF2
pip install spire
pip install spire.doc
pip install numpy
pip install scipy
pip install scikit-learn
pip install lftk
pip install spacy
python -m spacy download en_core_web_sm
call venv\Scripts\deactivate.bat