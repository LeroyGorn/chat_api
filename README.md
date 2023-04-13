# chat_api


1. Clone this repository.

2. Open your terminal.

3. Create a new virtual environment by typing the following command: "python3 -m venv env".

This will create a new directory named "env" in your current directory that contains all the necessary files for your virtual environment.

4. Activate the virtual environment by running the following command: "source env/bin/activate".

5. pip install -r requirements.txt

6. Create .env file near the "requirements.txt". Then navigate to chatty dir: "cd chatty/".
Run this command: "python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'"

Assign printed value to variable SECRET_KEY in .env file: SECRET_KEY=VALUE, without any quotes.

7. Then run: "python manage.py migrate", DB shoud be created.

8. Then run: "python manage.py loaddata fixture/data.json". Output should be: "Installed 104 object(s) from 1 fixture(s)".

9. Run: "python manage.py runserver". You can access admin panel using this creds:
email: leroygorn@gmail.com
pass: 1

OR

email: gorny@gmail.com
pass: 1

10. NOTE: All registered users has password: "1" for simplifying testing.

11. Better use postman to test this API. After login, you will receive two tokens. Use Bearer access token to provide authentication, while testing this API.

12. Almost all routes works only for authenticated user. So just login, to access all functionallity.

See ya !
