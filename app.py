from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

loan = []


@app.route("/")
def render_index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    loan_type = request.form["loan_type"]
    remaining_student_debt = int(request.form["remaining_student_debt"])
    annual_income = int(request.form["annual_income"])

    loan_data = {
        "loan_type": loan_type,
        "remaining_student_debt": remaining_student_debt,
        "annual_income": annual_income,
    }

    loan.append(loan_data)

    return redirect(url_for("result"))

def calculate_loan_repayment(loan_type, annual_income):
    thresholds = {
        "Plan 1": 22015,
        "Plan 2": 27295,
        "Plan 4": 27660,
        "Plan 5": 25000,
        "Postgraduate": 21000
    }

    rates = {
        "Plan 1": 0.09,
        "Plan 2": 0.09,
        "Plan 4": 0.09,
        "Plan 5": 0.09,
        "Postgraduate": 0.06
    }

    if loan_type in thresholds:
        threshold = thresholds[loan_type]
        rate = rates[loan_type]

        if annual_income > threshold:
            repayment = (annual_income - threshold) * rate
            return round(repayment, 2)  # Round to 2 decimal places for currency
        else:
            return 0
    else:
        return 0

@app.route("/loan_repayment_data")
def loan_repayment():
    return render_template("loan_repayment.html", data=loan_repayment_data)


# @app.route("/result")
# def result():
#     return render_template("result.html", degrees=degrees)


if __name__ == "__main__":
    app.run()