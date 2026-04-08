import os
from flask import Flask, request, Response
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# =========================
# CONFIG EMAIL
# =========================
EMAIL_FROM = "omntest923@gmail.com"
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

EMAIL_TO = [
    "rca.baar@omniasig.ro",
    "andrei.stefan@omniasig.ro",
    "Miruna.Chiva@omniasig.ro",
    "teodora.bineata@omniasig.ro"
]

# =========================
# CALE HTML
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE_DIR, "procedura_baar_omniasig.html")

@app.route("/", methods=["GET", "POST"])
def form():
    try:
        if request.method == "POST":

            nr_caz = request.form.get("nr_caz_baar", "")
            sasiu = request.form.get("sasiu_auto", "")
            data_start = request.form.get("data_start", "")

            msg = EmailMessage()
            msg["Subject"] = f"Procedura BAAR OMNIASIG – Caz BAAR {nr_caz}"
            msg["From"] = EMAIL_FROM
            msg["To"] = ", ".join(EMAIL_TO)
            msg.set_content(
                f"Nr. Caz BAAR: {nr_caz}\nȘasiu auto: {sasiu}\nDată: {data_start}"
            )

            # atașamente
            for f in request.files.values():
                if f.filename:
                    msg.add_attachment(
                        f.read(),
                        maintype="application",
                        subtype="octet-stream",
                        filename=f.filename
                    )

            # ✅ SMTP corect pentru Gmail în cloud
            smtp = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
            smtp.quit()

            return Response("✅ Documentele au fost trimise cu succes.", mimetype="text/plain")

        # GET
        with open(HTML_PATH, encoding="utf-8") as f:
            return Response(f.read(), mimetype="text/html")

    except Exception as e:
        # EROAREA EXACTĂ apare în Render Logs
        return Response(
            f"Internal Server Error SMTP: {str(e)}",
            status=500,
            mimetype="text/plain"
        )

if __name__ == "__main__":
    app.run()
