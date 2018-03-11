# MOOC Lession Retrieval System

Report: [here](https://drive.google.com/file/d/123E3r4JG0lmHxdD1ObTO_bKj9t5ixDpS/view?usp=sharing)

Discussion: [here](https://docs.google.com/document/d/1wTDBRWCuRBwWPIcieMeZ4cfdselPJ57jDcbJx3eiJeE/edit)

## Dependencies

* Python 3.6
  * python modules are listed in `requirements.txt`

## Step-by-step Set-up Procedure

* Install the dependencies: `pip install -r requirements.txt`
* Download subtitles of mit open courses: `python MITCrawler.py`
* Preprocess the subtitels `python preprocess_mit.py`
* Run the server: `python server.py`

## Test

* `python tests.py`