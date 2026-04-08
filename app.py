from flask import Flask, request
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

EMAIL_FROM = "formular.baar@omniasig.ro"
EMAIL_PASSWORD = "PAROLA_SMTP"

EMAIL_TO = [
    "rca.baar@omniasig.ro",
    "andrei.stefan@omniasig.ro",
    "Miruna.Chiva@omniasig.ro",
    "teodora.bineata@omniasig.ro"
]

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":

        # ✅ citim datele DIN formular (aici există!)
        nr_caz = request.form.get("nr_caz_baar")
        sasiu = request.form.get("sasiu_auto")
        data_start = request.form.get("data_start")
        intermediar = request.form.get("intermediar")
        cod_raf = request.form.get("cod_raf")
        tip_proprietar = request.form.get("tip_proprietar")
        proprietar_auto = request.form.get("proprietar_auto")

        # ✅ construim textul emailului
        text_email = f"""
Procedura BAAR OMNIASIG – documente primite

Nr. Caz BAAR: {nr_caz}
Șasiu auto: {sasiu}
Data start / valabilitate poliță: {data_start}

Intermediere: {intermediar}
Cod RAF: {cod_raf}

Tip proprietar: {tip_proprietar}
Proprietar auto: {proprietar_auto}
"""

        msg = EmailMessage()
        msg["Subject"] = f"Procedura BAAR OMNIASIG – Caz BAAR {nr_caz}"
        msg["From"] = EMAIL_FROM
        msg["To"] = ", ".join(EMAIL_TO)
        msg.set_content(text_email)

        # ✅ atașăm toate fișierele încărcate
        for file_key in request.files:
            f = request.files[file_key]
            if f and f.filename:
                path = os.path.join(UPLOAD_FOLDER, f.filename)
                f.save(path)
                with open(path, "rb") as file:
                    msg.add_attachment(
                        file.read(),
                        maintype="application",
                        subtype="octet-stream",
                        filename=f.filename
                    )

        # ✅ trimitem emailul
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)

        return "✅ Documentele au fost trimise cu succes."

    # ✅ afișăm formularul
    return open("procedura_baar_omniasig.html", encoding="utf-8").read()


if __name__ == "__main__":
    app.run()

