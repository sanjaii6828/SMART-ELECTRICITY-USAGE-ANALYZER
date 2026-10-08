import os
import sys
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, send_file
from sklearn.linear_model import LinearRegression

# Configure UTF-8 for console output on Windows if supported
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "electricity_data.csv")

# Support both 'template' and 'templates' directory names
TEMPLATE_DIR = os.path.join(BASE_DIR, "template")
if not os.path.exists(TEMPLATE_DIR):
    TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR
)


# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
def load_data():
    """Load electricity dataset from CSV file."""
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()

    df = pd.read_csv(DATA_FILE)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values(by="date").reset_index(drop=True)

    if "units" in df.columns:
        df["units"] = pd.to_numeric(df["units"], errors="coerce")
    if "temperature" in df.columns:
        df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce").fillna(25.0)
    if "appliances" in df.columns:
        df["appliances"] = pd.to_numeric(df["appliances"], errors="coerce").fillna(5).astype(int)

    return df


# -------------------------------------------------
# Electricity Cost Calculation
# -------------------------------------------------
def calculate_cost(units):
    """
    Slab-based electricity tariff calculation.
    - Up to 100 units: Rs. 2.50 / unit
    - Next 100 units (101-200): Rs. 3.50 / unit
    - Next 300 units (201-500): Rs. 5.00 / unit
    - Above 500 units: Rs. 7.00 / unit
    """
    try:
        units = float(units)
    except (ValueError, TypeError):
        return 0.0

    if units <= 0:
        return 0.0

    if units <= 100:
        cost = units * 2.50
    elif units <= 200:
        cost = (100 * 2.50) + ((units - 100) * 3.50)
    elif units <= 500:
        cost = (100 * 2.50) + (100 * 3.50) + ((units - 200) * 5.00)
    else:
        cost = (
            (100 * 2.50)
            + (100 * 3.50)
            + (300 * 5.00)
            + ((units - 500) * 7.00)
        )

    return round(cost, 2)


# -------------------------------------------------
# Generate Recommendation
# -------------------------------------------------
def generate_recommendation(average_units, peak_units):
    """Generate smart energy-saving recommendations."""
    if peak_units > average_units * 1.5:
        return (
            "High electricity spike detected. "
            "Check high-power appliances such as AC, water heater, "
            "washing machine, and refrigerator to prevent energy loss."
        )
    elif average_units > 18:
        return (
            "Your average electricity consumption is above optimal levels. "
            "Consider optimizing AC temperature and turning off idle appliances."
        )
    elif average_units > 13:
        return (
            "Your electricity consumption is moderate and stable. "
            "Switch off standby appliances to optimize your monthly utility bill."
        )
    else:
        return (
            "Your electricity consumption is highly efficient! "
            "Continue using 5-star energy rated appliances and LED fixtures."
        )


# -------------------------------------------------
# Perform Analysis & Prediction
# -------------------------------------------------
def perform_analysis(df):
    """Perform statistical analysis and ML-based usage forecasting."""
    if df.empty:
        return None

    total_units = round(float(df["units"].sum()), 2)
    average_units = round(float(df["units"].mean()), 2)
    highest_usage = round(float(df["units"].max()), 2)
    lowest_usage = round(float(df["units"].min()), 2)

    # Date with highest usage
    max_idx = df["units"].idxmax()
    max_row = df.loc[max_idx]
    peak_date = max_row["date"].strftime("%d-%m-%Y")
    peak_units = round(float(max_row["units"]), 2)

    # Lowest usage date
    min_idx = df["units"].idxmin()
    min_row = df.loc[min_idx]
    lowest_date = min_row["date"].strftime("%d-%m-%Y")

    # Estimated cost
    estimated_cost = calculate_cost(total_units)

    # Recommendation
    recommendation = generate_recommendation(average_units, highest_usage)

    # Usage status
    if average_units > 18:
        status = "High"
    elif average_units > 13:
        status = "Moderate"
    else:
        status = "Low"

    # Chart data
    chart_dates = df["date"].dt.strftime("%d-%m").tolist()
    chart_units = [round(float(val), 2) for val in df["units"].tolist()]
    chart_temps = [round(float(val), 1) for val in df["temperature"].tolist()]

    # ---------------------------------------------
    # Machine Learning Prediction (Next 7 Days)
    # ---------------------------------------------
    n_records = len(df)
    X = np.arange(n_records).reshape(-1, 1)
    y = df["units"].values

    model = LinearRegression()
    model.fit(X, y)

    future_days = np.arange(n_records, n_records + 7).reshape(-1, 1)
    raw_preds = model.predict(future_days)

    predictions = [round(max(0.0, float(val)), 2) for val in raw_preds]

    last_date = df["date"].max()
    future_dates_range = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=7
    )
    future_dates = [d.strftime("%d-%m") for d in future_dates_range]

    predicted_average = round(float(np.mean(predictions)), 2)
    predicted_cost = calculate_cost(predicted_average * 30)

    # Format historical records for frontend table
    records = []
    for _, row in df.iterrows():
        records.append({
            "date": row["date"].strftime("%Y-%m-%d"),
            "display_date": row["date"].strftime("%d %b %Y"),
            "units": round(float(row["units"]), 2),
            "temperature": round(float(row.get("temperature", 25)), 1),
            "appliances": int(row.get("appliances", 5)),
            "cost": calculate_cost(row["units"]),
        })

    return {
        "total_units": total_units,
        "average_units": average_units,
        "highest_usage": highest_usage,
        "lowest_usage": lowest_usage,
        "peak_date": peak_date,
        "peak_units": peak_units,
        "lowest_date": lowest_date,
        "estimated_cost": estimated_cost,
        "status": status,
        "recommendation": recommendation,
        "chart_dates": chart_dates,
        "chart_units": chart_units,
        "chart_temps": chart_temps,
        "future_dates": future_dates,
        "predictions": predictions,
        "predicted_average": predicted_average,
        "predicted_cost": predicted_cost,
        "records": records,
        "record_count": len(records),
    }


def print_summary(results):
    """Print structured summary to console."""
    print("=" * 60)
    print("       SMART ELECTRICITY USAGE ANALYZER")
    print("=" * 60)
    print(f"Total Usage           : {results['total_units']} kWh")
    print(f"Average Daily Usage   : {results['average_units']} kWh")
    print(f"Peak Usage            : {results['highest_usage']} kWh (on {results['peak_date']})")
    print(f"Lowest Usage          : {results['lowest_usage']} kWh (on {results['lowest_date']})")
    print(f"Estimated Cost        : Rs. {results['estimated_cost']}")
    print(f"Energy Status         : {results['status']}")
    print(f"Smart Recommendation  : {results['recommendation']}")
    print("-" * 60)
    print("AI Usage Prediction (Next 7 Days):")
    for date_str, pred_val in zip(results['future_dates'], results['predictions']):
        print(f"  * {date_str} : {pred_val} kWh")
    print(f"Predicted Daily Avg   : {results['predicted_average']} kWh")
    print(f"Predicted Monthly Cost: Rs. {results['predicted_cost']}")
    print("=" * 60)


# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.route("/")
def home():
    df = load_data()
    if df.empty:
        return "Dataset not found or empty! Please check electricity_data.csv.", 404

    results = perform_analysis(df)
    return render_template(
        "index.html",
        total_units=results["total_units"],
        average_units=results["average_units"],
        highest_usage=results["highest_usage"],
        lowest_usage=results["lowest_usage"],
        peak_date=results["peak_date"],
        peak_units=results["peak_units"],
        lowest_date=results["lowest_date"],
        estimated_cost=results["estimated_cost"],
        status=results["status"],
        recommendation=results["recommendation"],
        chart_dates=results["chart_dates"],
        chart_units=results["chart_units"],
        chart_temps=results["chart_temps"],
        future_dates=results["future_dates"],
        predictions=results["predictions"],
        predicted_average=results["predicted_average"],
        predicted_cost=results["predicted_cost"],
        records=results["records"],
        record_count=results["record_count"]
    )


@app.route("/add", methods=["POST"])
def add_data():
    try:
        date = request.form["date"]
        units = float(request.form["units"])
        temperature = float(request.form["temperature"])
        appliances = int(request.form["appliances"])

        new_data = pd.DataFrame({
            "date": [date],
            "units": [units],
            "temperature": [temperature],
            "appliances": [appliances]
        })

        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            df = pd.concat([df, new_data], ignore_index=True)
        else:
            df = new_data

        df.to_csv(DATA_FILE, index=False)
        return render_template("success.html")
    except Exception as e:
        return f"Error adding data: {str(e)}", 400


@app.route("/export")
def export_data():
    if os.path.exists(DATA_FILE):
        return send_file(DATA_FILE, as_attachment=True, download_name="electricity_data.csv")
    return "File not found", 404


# -------------------------------------------------
# Run Application
# -------------------------------------------------
if __name__ == "__main__":
    df = load_data()
    if not df.empty:
        results = perform_analysis(df)
        print_summary(results)
    print("\nStarting Web Application on http://127.0.0.1:5000 ...")
    app.run(debug=True)
