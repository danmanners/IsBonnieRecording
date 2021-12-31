import ast, json, time
from flask import Flask, Response, request
from blink1.blink1 import Blink1

# Flask Setup
app = Flask(__name__)

# Set the
isrecording = {"recording": False}

# Print Blink Serial Information
blink1_serials = Blink1.list()
if blink1_serials:
    print(f"blink(1) devices found: {blink1_serials}")
else:
    print("blink(1) device not found! Connect it and try running this again.")
    quit()

# Startup function: turn the LED off
def turn_led_off():
    b1 = Blink1()
    b1.fade_to_color(0, "black")
    b1.close()


# Health Check
@app.route("/api/health", methods=["GET", "HEAD"])
def healthcheck():
    blink1_serials = Blink1.list()
    print(blink1_serials)
    if blink1_serials:
        return Response(f"Healthy; device connected: {blink1_serials[0]}", status=200)
    else:
        return Response("Not Ready", status=503)


@app.route("/api/recording", methods=["GET", "POST"])
def recording():
    if request.method == "GET":
        return Response(
            json.dumps(isrecording), status=200, mimetype="application/json"
        )
    if request.method == "POST":
        data = ast.literal_eval(request.get_data().decode("utf-8"))

        # Update if Bonnie's recording or not
        isrecording.update(data)

        # If recording True, turn Purple
        if isrecording["recording"] is True:
            b1 = Blink1()
            b1.fade_to_color(500, "purple")
            b1.close()

        elif isrecording["recording"] is False:
            b1 = Blink1()
            b1.fade_to_color(500, "black")
            b1.close()

        return Response(
            json.dumps(isrecording), status=200, mimetype="application/json"
        )


if __name__ == "__main__":
    try:
        app.run(debug=True)
        turn_led_off()
    except KeyboardInterrupt:
        print("killing the service.")
        quit()
