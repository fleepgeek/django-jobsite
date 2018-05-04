# django-jobsite

This is a job recruitment site powered by django. The entire project was created using django's Class Based Views (CBV). This is still a work in progress but would give you an understanding of creating related sites like this. 

## Features
* Custom User Model
* Stripe Integration
* User Roles
* Ajax Forms
* Custom Model Managers
* Bulma Framework for Design

## Installation

Create a folder on your computer then clone this repo with this command:

```bash
git clone https://github.com/fleepgeek/django-jobsite.git
#Next
cd django-jobsite/src
```
I used pipenv to create a virtual environment, so you install pipenv globally on your computer:
```bash
pip install pipenv
```

Create a  ``.env`` file and include your stripe details (You must have a stripe account):
```
STRIPE_PUB_KEY=your_public_key
STRIPE_SECRET_KEY=your_secret_key
```

Create a new virtual environment:
```bash
pipenv shell
```

Next, install required packages stored in the ``Pipfile.lock`` file using the ``sync`` command.
```bash
pipenv sync
```

Then you run your migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
You're good to go :sparkles:

## Shameless Plug Here :see_no_evil:
If you read this guide up to this point, you should definately checkout my [YouTube Channel](https://www.youtube.com/channel/UCXX74aetH0OPVYNxxcVpTJw) for Django related tutorials. 
