from flask import Flask, render_template, request, redirect, url_for
import qrcode
import os

app = Flask(__name__)

hospitals = []
cases = []

# create qr folder
if not os.path.exists("static/qr"):
    os.makedirs("static/qr")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/hospital/register", methods=["GET","POST"])
def register_hospital():

    if request.method == "POST":

        name = request.form["name"]
        upi = request.form["upi_id"]

        hospitals.append({
            "name": name,
            "upi": upi
        })

        return redirect(url_for("home"))

    return render_template("register_hospital.html")


@app.route("/case/create", methods=["GET","POST"])
def create_case():

    if request.method == "POST":

        patient = request.form["patient_name"]
        amount = request.form["amount"]
        hospital = request.form["hospital"]

        cases.append({
            "patient": patient,
            "amount": amount,
            "hospital": hospital
        })

        return redirect(url_for("view_cases"))

    return render_template("create_case.html", hospitals=hospitals)


@app.route("/cases")
def view_cases():
    return render_template("view_cases.html", cases=cases)


@app.route("/donate/<int:case_id>", methods=["GET","POST"])
def donate(case_id):

    case = cases[case_id]

    hospital_upi = None
    for h in hospitals:
        if h["name"] == case["hospital"]:
            hospital_upi = h["upi"]

    qr_path = None

    if request.method == "POST":

        donate_amount = request.form["donate_amount"]

        upi_link = f"upi://pay?pa={hospital_upi}&pn={case['hospital']}&am={donate_amount}&cu=INR"

        img = qrcode.make(upi_link)

        qr_path = f"static/qr/case{case_id}.png"
        img.save(qr_path)

        return render_template("donate.html", case=case, qr=qr_path)

    return render_template("donate.html", case=case, qr=None)


if __name__ == "__main__":
    app.run(debug=True)
