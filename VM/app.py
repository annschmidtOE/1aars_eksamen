from flask import Flask, render_template
import base64
from io import BytesIO
from matplotlib.figure import Figure
from matplotlib.dates import AutoDateLocator, DateFormatter
from get_costumer_count import get_customer_count
from get_satisfaction import get_satisfaction_count
import logging

app = Flask(__name__)

@app.route("/index")
def home():
    return render_template("index.html")

def get_costumer_data():
    counts, dates = get_customer_count()
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis="x", which="both", rotation=30)
    ax.set_facecolor("#fff")

    ax.plot(dates, counts, linestyle="dashed", c="orange", linewidth="1.7", marker="D", mec="green", ms=7)
    ax.set_xlabel("Counts")
    ax.set_ylabel("Dates")
    fig.patch.set_facecolor("#fff")
    ax.tick_params(axis="x", colors="black")
    ax.tick_params(axis="y", colors="green")
    ax.spines["left"].set_color("orange")
    ax.spines["right"].set_color("orange")
    ax.spines["top"].set_color("black")
    ax.spines["bottom"].set_color("black")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data1 = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    return data1



def get_data_satisfaction():
    satisfaction, dates = get_satisfaction_count()

    logging.debug(f"Satisfaction values: {satisfaction}")
    logging.debug(f"Dates: {dates}")

    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis="x", which="both", rotation=30)
    ax.set_facecolor("#fff")

    satisfaction_labels = {1: 'utilfreds', 2: 'ok', 3: 'tilfreds'}
    mapped_satisfaction = [satisfaction_labels.get(s, 'unknown') for s in satisfaction]

    ax.plot(dates, satisfaction, linestyle="dashed", c="orange", linewidth="1.7", marker="D", mec="green", ms=7)
    ax.set_xlabel("Date and Time")
    ax.set_ylabel("Satisfaction")
    fig.patch.set_facecolor("#fff")
    ax.tick_params(axis="x", colors="black")
    ax.tick_params(axis="y", colors="green")
    ax.spines["left"].set_color("orange")
    ax.spines["right"].set_color("orange")
    ax.spines["top"].set_color("black")
    ax.spines["bottom"].set_color("black")

    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(['utilfreds', 'ok', 'tilfreds'])

    fig.autofmt_xdate()

    ax.xaxis.set_major_locator(AutoDateLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M:%S'))

    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    data = base64.b64encode(buf.getvalue()).decode("ascii")

    return data

@app.route("/costumer_count")
def costumer_count():
    image_data = get_costumer_data()
    return render_template("costumer_count.html", data=image_data)

@app.route("/satisfaction")
def satisfaction_count():
    image_data = get_data_satisfaction()
    return render_template("satisfaction.html", data=image_data)


app.run(debug=True, host="0.0.0.0")

