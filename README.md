# Webpage project - eteenpain.com:
This is a Python Flask application for Team-Yonex webpages, www.eteenpain.com.

It supports media folders with downloads/uploads, user login and registration/sign-up features and user profiles.

# Build:
Tested on python 3.8+ version. To run the application locally first activate your python environment and then run below commands in command line in your desired directory.

```
git clone https://github.com/leikeri/eteenpain.git
cd eteenpain
install_and_run.bat
```

It installs required modules to your environment and the database used for user logins and registrations. There are additional columns which may be used for user profile pages.

Webpage www.eteenpain.com currently runs on linux server and some changes had to be made in order to get it up and running. For example, path definitions in helper.py file had to be modified. Also, route('/home') didn't work via index route('/'). It was circumvented by replacing index blueprint with route('/') with the main route('/') with kick_off-function, which renders the home template "koti.html".

