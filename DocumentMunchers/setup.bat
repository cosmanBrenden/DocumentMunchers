@echo off

cd FrontEnd
npm i
cd ..

@REM python -m venv venv
@REM call venv\Scripts\activate.bat
@REM pip install flask
@REM pip install flask_cors
@REM pip install transformers
@REM pip install sentence_transformers
@REM pip install pdfminer
@REM pip install pdfminer.six
@REM pip install PyPDF2
@REM pip install spire
@REM pip install spire.doc
@REM pip install numpy
@REM pip install scipy
@REM pip install scikit-learn
@REM pip install lftk
@REM pip install spacy
@REM pip install nltk
pip install -r requirements.txt
python -m spacy download en_core_web_sm
@REM call venv\Scripts\deactivate.bat