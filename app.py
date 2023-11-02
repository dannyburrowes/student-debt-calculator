from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

loan = []


@app.route("/")
def render_index():
    return render_template("index.html")


# @app.route("/calculate", methods=["POST"])
# def calculate():
#
#
#     loan_data = {
#         "loan_type": loan_type,
#         "remaining_student_debt": remaining_student_debt,
#         "annual_income": annual_income,
#     }
#
#     loan.append(loan_data)


@app.route("/calculate", methods=["POST"])
def calculate_loan_repayment():
    try:
        loan_type = request.form["loan_type"]
        remaining_student_debt = int(request.form["remaining_student_debt"])
        annual_income = int(request.form["annual_income"])
        today = datetime.date.today()
        year = today.year
        total_repayment = 0
        total_interest = 0

        thresholds = {
            "Type 1": 22015,
            "Type 2": 27295,
            "Type 4": 27660,
            "Postgraduate": 21000
        }

        repayment_rates = {
            "Type 1": 0.09,
            "Type 2": 0.09,
            "Type 4": 0.09,
            "Postgraduate": 0.06
        }

        interest_rates = {
            "Type 1": 1.25,
            "Type 4": 1.25,
            "Postgraduate": 6
        }

        threshold = thresholds[loan_type]
        repayment_rate = repayment_rates[loan_type]
        interest_rate = 0
        if loan_type != "Type 2":
            interest_rate = interest_rates[loan_type]
        elif loan_type == "Type 2":
            if threshold < annual_income <= 49130:
                interest_rate = round(((annual_income - threshold) * 0.00013739) + 1.5, 2)
            elif annual_income > 49130:
                interest_rate = 4.5
            elif annual_income <= threshold:
                interest_rate = 1.5


        if annual_income > threshold:
            annual_repayment = round((annual_income - threshold) * repayment_rate, 2)
        else:
            annual_repayment = 0

        remaining_student_debts_list = [remaining_student_debt]
        total_repayments_list = ["-"]
        total_interests_list = ["-"]
        interest_this_year_list = ["-"]
        annual_repayments_list = ["-"]
        interest_rates_list = ["-"]
        annual_incomes_list = ["-"]

        for i in range(0, 30):
            year += 1
            interest_this_year = remaining_student_debt * (interest_rate * 0.01)
            remaining_student_debt = remaining_student_debt + interest_this_year - annual_repayment
            remaining_student_debts_list.append(round(remaining_student_debt, 2))
            annual_repayments_list.append(round(annual_repayment, 2))
            interest_rates_list.append(interest_rate)
            annual_incomes_list.append(annual_income)
            total_repayment += annual_repayment
            total_repayments_list.append(round(total_repayment, 2))
            total_interest += interest_this_year
            total_interests_list.append(round(total_interest, 2))
            interest_this_year_list.append(round(interest_this_year, 2))

        # HELLO changes


        # return redirect(url_for("result"))
        return render_template("result.html", loan_type=loan_type, annual_income=annual_incomes_list, remaining_student_debt=remaining_student_debts_list, interest_rate=interest_rates_list, annual_repayment=annual_repayments_list, interest_this_year=interest_this_year_list, total_repayment=total_repayments_list, total_interest=total_interests_list)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

# @app.route("/result")
# def result():
#     return render_template("result.html")


if __name__ == "__main__":
    app.run(debug=False)
