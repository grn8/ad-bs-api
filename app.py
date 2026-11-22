from flask import Flask, request, jsonify
from datetime import datetime, date
import nepali_datetime

app = Flask(__name__)

# Correct month names
NEPALI_MONTHS = [
    "", "Baisakh", "Jestha", "Ashad", "Shrawan", "Bhadra", "Ashwin",
    "Kartik", "Mangsir", "Poush", "Magh", "Falgun", "Chaitra"
]

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "AD to BS Converter API",
        "endpoints": {
            "GET /ad-to-bs?date=YYYY-MM-DD": "Convert AD → BS",
            "GET /today": "Today's BS date (Nepal time)"
        }
    })

@app.route("/ad-to-bs", methods=["GET"])
def ad_to_bs():
    ad_date_str = request.args.get("date")

    if not ad_date_str:
        return jsonify({"error": "Missing 'date' parameter. Use ?date=YYYY-MM-DD"}), 400

    try:
        # Parse AD date
        ad_date = datetime.strptime(ad_date_str, "%Y-%m-%d").date()

        # Convert using nepali_datetime
        bs_date = nepali_datetime.date.from_datetime_date(ad_date)

        return jsonify({
            "ad_date": ad_date_str,
            "bs_date": f"{bs_date.year}-{bs_date.month:02d}-{bs_date.day:02d}",
            "bs_year": bs_date.year,
            "bs_month": bs_date.month,
            "bs_month_name": NEPALI_MONTHS[bs_date.month],
            "bs_day": bs_date.day
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/today", methods=["GET"])
def today():
    """Return today's BS date using Nepal timezone (Asia/Kathmandu)"""
    try:
        # Get current date in Nepal
        nepal_today = nepali_datetime.date.today()

        return jsonify({
            "ad_date": date.today().isoformat(),
            "bs_date": f"{nepal_today.year}-{nepal_today.month:02d}-{nepal_today.day:02d}",
            "bs_year": nepal_today.year,
            "bs_month": nepal_today.month,
            "bs_month_name": NEPALI_MONTHS[nepal_today.month],
            "bs_day": nepal_today.day,
            "timezone": "Asia/Kathmandu"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
