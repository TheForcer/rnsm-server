# rnsm-server
Updated Server part of my rnsm programming project for Incident Response & Malware Defense.

The client can befound here: https://github.com/TheForcer/rnsm-client

# Setup
Make sure that you are using Python >3.7 and have pip available to install the requirements:

1. Clone the source code with `git clone https://github.com/TheForcer/rnsm-server`

2. Checkout the correct branch with `git checkout incidentresponse`

3. Install the Python requirements using pip with `pip3 install -r requirements.txt`

4. Change the default "rnsm" password in `app/__init__.py` to a password of your choice.

5. You need to have a Minio S3 server running elsewhere, which acts as a upload endpoint for data exfiltration:
    - Enter the Minio Admin Server details at the top of the `app/routes.py` file
    - The Minio client binary needs to be available in the PATH with the name `mclient`

6. Make sure the packed & obfuscated ransom.exe/exfil.exe stages from the client are available in the respective folders in `app/static`

7. Run the server with `python3 run.py`

The webinterface is then reachable at http://{YOUR_IP}:5000/
Make sure to put a proxy such as nginx/Apache2 in front of the app for TLS termination, advanced logging etc.
