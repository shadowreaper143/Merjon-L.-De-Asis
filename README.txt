SPACE INVADERS
LOGIN + REGISTRATION + MYSQL LEADERBOARD


========================================
1. INSTALL PYTHON
========================================

Install Python 3.10 or newer.


========================================
2. INSTALL PACKAGES
========================================

Open Command Prompt inside the project folder.

Run:

pip install -r requirements.txt


========================================
3. START MYSQL
========================================

If you are using XAMPP:

1. Open XAMPP
2. Start Apache if needed
3. Start MySQL


========================================
4. MYSQL SETTINGS
========================================

Default settings:

Host:
localhost

Port:
3306

Username:
root

Password:
empty

Database:
space_invaders_db


If your MySQL root account has a password,
edit managers/database.py.

Change:

password=""

to:

password="YOUR_PASSWORD"


========================================
5. RUN THE GAME
========================================

Run:

python main.py


========================================
6. CREATE ACCOUNT
========================================

When the game starts:

Click:

Create an account

Enter:

Username
Email
Password
Confirm Password

Then click:

REGISTER


========================================
7. LOGIN
========================================

Enter:

Username
Password

Then click:

LOGIN


========================================
8. PLAY
========================================

Keyboard:

LEFT ARROW  = Move left
RIGHT ARROW = Move right
SPACE       = Shoot
ESC         = Settings


========================================
9. SCORE
========================================

Each destroyed enemy gives:

10 points


When the player loses:

The score is automatically saved
to MySQL.


========================================
10. LEADERBOARD
========================================

The leaderboard retrieves the
highest score for every registered
player directly from MySQL.


========================================
IMPORTANT
========================================

Keep the assets folder in the
correct location.

assets/images/
assets/sounds/