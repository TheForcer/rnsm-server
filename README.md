# rnsm-server
Server part of my rnsm programming project.

The client can be found here: https://github.com/TheForcer/rnsm-client

# Setup

Make sure you are using Python 3.8 and have pip available to install the requirements:

1. Clone the source with `git clone https://github.com/TheForcer/rnsm-server`.

2. Install the Python requirements using pip with `pip3 install -r requirements.txt`.

3. Change the default password "rnsm" in `app/__init__.py` to a password of your choice.

4. Start the server with `python3 run.py`.

The web interface will then be accessible at http://{YOUR_IP}:5000/.
Make sure you put a proxy like nginx/Apache2 in front of the application for TLS termination, advanced logging etc.
