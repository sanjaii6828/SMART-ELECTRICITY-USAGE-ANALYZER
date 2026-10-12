# ⚡ Smart Electricity Usage Analyzer

## 📌 Project Description

The **Smart Electricity Usage Analyzer** is a Python-based web application that analyzes electricity consumption, estimates electricity costs, predicts future energy usage using Machine Learning, and provides smart energy-saving recommendations.

The application uses a CSV dataset to monitor daily electricity consumption, average usage, peak usage, temperature, and the number of appliances. It provides an interactive dashboard with charts and allows users to add new electricity usage records.

## 🎯 Objectives

* Analyze daily electricity consumption.
* Calculate total and average electricity usage.
* Identify peak and minimum consumption.
* Estimate electricity costs.
* Predict electricity usage for the next seven days.
* Generate energy-saving recommendations.
* Display consumption statistics through an interactive dashboard.
* Allow users to add new electricity records.

## ✨ Features

* **Electricity Usage Analysis:** Calculates total, average, highest, and lowest consumption.
* **Cost Estimation:** Estimates electricity expenses based on configurable example tariff rates.
* **Machine Learning Prediction:** Uses Linear Regression to predict electricity consumption for the next seven days.
* **Interactive Dashboard:** Displays electricity usage statistics and charts.
* **Peak Usage Detection:** Identifies the date with the highest electricity consumption.
* **Smart Recommendations:** Provides suggestions based on usage patterns, temperature, and appliance count.
* **Add New Records:** Allows users to enter electricity usage data through a web form.
* **CSV Data Management:** Stores and processes electricity consumption records.
* **Responsive Interface:** Provides a user-friendly web interface.

## 🛠️ Technologies Used

| Technology     | Purpose                             |
| -------------- | ----------------------------------- |
| Python         | Application development             |
| Flask          | Web application framework           |
| Pandas         | Dataset processing and analysis     |
| NumPy          | Numerical calculations              |
| Scikit-learn   | Machine Learning and prediction     |
| HTML5          | Dashboard structure                 |
| CSS3           | Dashboard styling                   |
| Chart.js       | Data visualization                  |
| CSV            | Electricity usage data storage      |
| VS Code        | Development environment             |
| Git and GitHub | Version control and project hosting |

## 📂 Project Structure

```text
Smart-Electricity-Usage-Analyzer/
│
├── .gitignore
├── app.py
├── electricity_data.csv
├── index.html
├── requirements.txt
├── style.css
├── success.html
├── test.py
└── README.md
```

## ⚙️ System Requirements

* Python 3.10 or later recommended
* Visual Studio Code
* pip package manager
* A modern web browser
* Internet connection for loading Chart.js from its CDN

## 🚀 Installation and Setup

### Step 1: Clone the Repository

If the project is hosted on GitHub, run:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Alternatively, download the project ZIP file and extract it to your computer.

### Step 2: Open the Project

Open the project folder in Visual Studio Code.

Open the integrated terminal using:

```text
Ctrl + `
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not yet populated, install the required libraries using:

```bash
pip install flask pandas numpy scikit-learn
```

### Step 6: Verify the Project Files

Ensure that the project contains:

* `app.py`
* `electricity_data.csv`
* `index.html`
* `style.css`
* `success.html`
* `requirements.txt`

The HTML templates and CSS files must be placed in the locations expected by `app.py`.

For a conventional Flask project, the structure is:

```text
project/
├── app.py
├── electricity_data.csv
├── requirements.txt
├── test.py
├── templates/
│   ├── index.html
│   └── success.html
└── static/
    └── style.css
```

If your files are currently in the project root, move them into the appropriate folders or update the Flask configuration accordingly.

### Step 7: Run the Application

```bash
python app.py
```

### Step 8: Open the Dashboard

Open the following URL in your browser:

```text
http://127.0.0.1:5000
```

The dashboard will display electricity consumption statistics, charts, predictions, and recommendations.

## 📊 Dataset Description

The application uses `electricity_data.csv` to store daily electricity consumption information.

| Column        | Description                             |
| ------------- | --------------------------------------- |
| `date`        | Date of electricity consumption         |
| `units`       | Electricity consumed in kWh             |
| `temperature` | Recorded temperature in degrees Celsius |
| `appliances`  | Number of appliances recorded           |

### Sample Dataset

```csv
date,units,temperature,appliances
2026-09-01,12.5,28,5
2026-09-02,13.2,29,6
2026-09-03,11.8,27,4
2026-09-04,15.4,30,7
2026-09-05,16.2,31,8
```

The sample records are illustrative. Actual results depend on the dataset provided.

## 🤖 Machine Learning Methodology

The project uses **Linear Regression** to estimate future electricity consumption.

### Workflow

1. Load the electricity dataset.
2. Convert dates and numerical columns into appropriate data types.
3. Assign a sequential day number to each record.
4. Train a Linear Regression model using the day number and recorded electricity usage.
5. Generate predictions for the next seven days.
6. Display the predicted usage through a dashboard chart.

### Prediction Formula

Linear Regression models the relationship between the input variable and the predicted value as:

```text
y = mx + b
```

Where:

* `y` represents predicted electricity consumption.
* `x` represents the day number.
* `m` represents the learned slope.
* `b` represents the intercept.

**Note:** This is a basic educational prediction model. Its accuracy depends on the quality and quantity of historical data. It does not automatically account for seasonality, appliance schedules, or changing household behavior.

## 💰 Electricity Cost Estimation

The application calculates estimated electricity costs using example slab-based rates.

The example rates in the application are:

* First 100 units: ₹2.50 per unit
* Next 100 units: ₹3.50 per unit
* Next 300 units: ₹5.00 per unit
* Units above 500: ₹7.00 per unit

These rates are illustrative and may not match the actual electricity tariff applicable to a household.

The displayed cost is an estimate, not an official electricity bill. Actual bills may include fixed charges, taxes, subsidies, and other tariff-specific rules.

## 💡 Smart Recommendations

The system generates suggestions based on the recorded consumption pattern.

Examples include:

* Reduce unnecessary appliance usage.
* Switch off unused electrical devices.
* Monitor days with unusually high consumption.
* Use air conditioners efficiently during hot weather.
* Consider energy-efficient appliances.
* Review consumption trends regularly.

These recommendations are rule-based suggestions rather than guaranteed energy savings.

## 🧪 Testing

The project includes `test.py` for basic testing.

Activate the virtual environment and run:

```bash
python test.py
```

For manual application testing:

1. Start the Flask application.
2. Open the dashboard in a browser.
3. Verify the displayed electricity statistics.
4. Check whether the usage chart appears.
5. Verify the seven-day prediction chart.
6. Add a new electricity usage record.
7. Confirm that the record is saved to the CSV file.
8. Refresh the dashboard and check the updated results.

## 🔒 Data and Security

* The application stores its sample data locally in a CSV file.
* Do not upload personal or sensitive electricity usage information publicly.
* Debug mode is intended for local development only.
* Disable Flask debug mode before deploying the application publicly.
* Validate user input before saving records to prevent invalid data.

## 🔮 Future Enhancements

* Integrate smart meters for automatic data collection.
* Support Excel and additional dataset formats.
* Add monthly and yearly consumption reports.
* Compare consumption across different months.
* Implement anomaly detection for unusual electricity usage.
* Add user authentication and personalized dashboards.
* Provide downloadable reports in CSV or PDF format.
* Integrate real electricity tariff structures.
* Improve prediction performance with larger historical datasets.
* Deploy the application to a cloud platform.

## 🎓 Applications

* Household electricity monitoring
* College and educational projects
* Energy consumption analysis
* Electricity cost estimation
* Energy conservation awareness
* Basic electricity demand forecasting

## 👨‍💻 Project Information

**Project Name:** Smart Electricity Usage Analyzer

**Domain:** Python, Data Analytics, Machine Learning

**Framework:** Flask

**Machine Learning Algorithm:** Linear Regression

**Data Source:** CSV dataset

**Interface:** Web-based dashboard

**Development Tool:** Visual Studio Code

## 📜 License

This project is intended for educational and learning purposes. You may modify and extend the source code for academic or personal use.

## 🙏 Acknowledgements

Thanks to the Python, Flask, Pandas, NumPy, Scikit-learn, and Chart.js communities for providing the tools and documentation used in developing this project.

---

**Smart Electricity Usage Analyzer — Analyze Consumption, Predict Usage, and Encourage Smarter Energy Decisions.**
