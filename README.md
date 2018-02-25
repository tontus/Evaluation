## Requirements
* [Python 3](https://www.python.org/downloads/) 
* [Django](https://www.djangoproject.com/download/) 
* Celery[v3.1.24]: `$ pip install celery==3.1.24`
* Redis
	* [For windows](https://github.com/MicrosoftArchive/redis/releases)
	* [Other](https://redis.io/download) 
* Run `$ pip install -r requirements.txt` to install otherr requirements
* nltk dependencies 'brown', 'punkt', 'wordnet'
	`$ python
	>>> import nltk
	>>> nltk.download('brown')
	>>> nltk.download('punkt')
	>>> nltk.download('wordnet')`

## Usage
* Run `$ redis-server`
* Open another terminal in the project folder and run `$ python manage.py runserver`
* Open another terminal in the project folder and run `$ celery worker -A Evaluation --loglevel=debug --concurrency=4`
