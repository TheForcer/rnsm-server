# rnsm-server
Server part of my rnsm programming project.

The client can befound here: https://github.com/TheForcer/rnsm-client

# Setup
Make sure that you are using Python 3.8 and have pip available to install the requirements:

1. Clone the source code with `git clone https://github.com/TheForcer/rnsm-server`

2. Install the Python requirements using pip with `pip3 install -r requirements.txt`

3. Change the default "rnsm" password in `app/__init__.py` to a password of your choice.

4. Run the server with `python3 run.py`

The webinterface is then reachable at http://{YOUR_IP}:5000/
Make sure to put a proxy such as nginx/Apache2 in front of the app for TLS termination, advanced logging etc.
