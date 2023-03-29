
# Simple IP Logger 

Written with Django framework in Python interpreter. I created this project only for EDUCATIONAL purposes this means in code can be some unoptimized parts of code.
The main idea:
- Create link from panel
- Send link to people with social engineering tools


## Features

- Create links with redirects and some text
- Multi account
- Simple web panel



## Installation (Linux based OS)

Use this commands in root directory of project

```bash
    python3 -m venv venv &&
    source venv/bin/activate && 
    python3 -m pip install -r requirements.txt
```
Recommendations: change **SECRET_KEY** in iplog/settings.py

Next, you must set **ALLOWED_HOSTS** in iplog/settings.py with your public IP. For example: **ALLOWED_HOSTS = ["65.43.345.232"]** 

After that, you must set up credentials for MySQL database(check iplog/settings.py).

## Run
```bash
 python3 manage.py createsuperuser && python3 manage.py runserver 80 
 ```


## Issues 

If you found a problem or have an idea you are welcome to create *Issue*

## Screenshots
User panel
![App Screenshot](https://i.imgur.com/YDvHFb1.png)

View results
![App Screenshot](https://i.imgur.com/xWtgthh.png)

