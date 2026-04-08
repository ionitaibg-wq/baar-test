import os
from flask import Flask, request, Response
from email.message import EmailMessage

app = Flask(__name__)

# =========================
# CONFIG EMAIL (păstrat, dar NU trimitem)
# =========================
EMAIL_FROM = "omntest923@gmail.com"
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")  # NU se folosește în test

EMAIL_TO = [
    "rca.baar@omniasig.ro",
    "andrei.stefan@omniasig.ro",
    "Miruna.Chiva@omniasig.ro",
    "teodora.bineata@omniasig.ro"
]

# =========================
# CALE ABSOLUTĂ HTML
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE_DIR, "procedura_baar_omniasig.html")

# =========================
# ROUTA PRINCIPALĂ
# =========================
@app.route("/", methods=["GET", "POST"])
def form():
    try:
        if request.method == "POST":

            # -------- date din formular --------
            nr_caz = request.form.get("nr_caz_baar", "")
            sasiu = request.form.get("sasiu_auto", "")
            data_start = request.form.get("data_start", "")
            intermediar = request.form.get("intermediar", "")
            cod_raf = request.form.get("cod_raf", "")
            tip_proprietar = request.form.get("tip_proprietar", "")
            proprietar_auto = request.form.get("proprietar_auto", "")

            # -------- construim email (doar în memorie) --------
            text_email = f"""
Procedura BAAR OMNIASIG – documente primite (TEST – fără trimitere email)

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

            # -------- atașamente (test) --------
            for f in request.files.values():
                if f and f.filename:
                    msg.add_attachment(
                        f.read(),
                        maintype="application",
                        subtype="octet-stream",
                        filename=f.filename
                    )

            # ❌ TRIMITERE EMAIL DEZACTIVATĂ (TEST)
            # import smtplib
            # with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            #     smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            #     smtp.send_message(msg)

            return Response(
                "✅ Formular trimis cu succes (TEST – fără email).",
                mimetype="text/plain"
            )

        # -------- GET: afișare formular --------
        with open(HTML_PATH, encoding="utf-8") as f:
            return Response(f.read(), mimetype="text/html")

    except Exception as e:
        # afișăm eroarea exactă în caz de problemă
        return Response(f"Internal Server Error: {str(e)}", status=500)


# =========================
# START APLICAȚIE
# =========================
if __name__ == "__main__":
    app.run()
