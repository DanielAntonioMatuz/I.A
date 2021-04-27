import time

from flask import Flask, render_template
# from flask import render_template
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
value = []
i = 0

value.append(0)

@app.route('/')
def homepage():
    i = 1
    value[0] += i
    return render_template("index.html", title=value[0], description="Flask")


def updateData():
    while True:
        i = i + 1
        value[0] = i
        print("AAA")
        #time.sleep(5)

if __name__ == '__main__':
    app.run()

