from flask import Flask, request, jsonify
from nepali_datetime import date as nep_date
import datetime

app = Flask(__name__)

@app.route("/ad-to-bs", methods=["GET"])
def ad_to_bs():
    ad_date_str = request.args.get("date")  # Format: yyyy-mm-dd
    try:
        ad_date = datetime.datetime.strptime(ad_date_str, "%Y-%m-%d").date()
        bs_date = nep_date.from_datetime_date(ad_date)

        # Nepali month names (index 1 to 12)
        nepali_months = [
            "", "Baisakh", "Jestha", "Ashad", "Shrawan", "Bhadra", "Ashwin",
            "Kartik", "Mangsir", "Poush", "Magh", "Falgun", "Chaitra"
        ]
        bs_month_name = nepali_months[bs_date.month]

        return jsonify({
            "ad_date": ad_date_str,
            "bs_date": bs_date.strftime("%Y-%m-%d"),
            "bs_year": bs_date.year,
            "bs_month": bs_date.month,
            "bs_month_name": bs_month_name,
            "bs_day": bs_date.day
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run()
