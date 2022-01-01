import ast, json
from flask import Flask, Response, request
from flask_cors import CORS
from blink1.blink1 import Blink1

# Flask Setup
app = Flask(__name__)
CORS(app)

# Set the default state; we don't need no stinkin' database!
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


# Health Check Endpoint
@app.route("/api/health", methods=["GET", "HEAD"])
def healthcheck():
    blink1_serials = Blink1.list()
    print(blink1_serials)
    if blink1_serials:
        return Response(f"Healthy; device connected: {blink1_serials[0]}", status=200)
    else:
        return Response("Not Ready", status=503)


# API Recording Endpoint
@app.route("/api/recording", methods=["GET", "POST", "OPTIONS"])
def recording():
    if request.method == "OPTIONS":
        response = Response(
            status=204,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": ["GET", "POST", "OPTIONS"],
                "Access-Control-Allow-Headers": [
                    "Charset",
                    "Content-Type",
                    "Access-Control-Allow-Origin",
                    "Access-Control-Allow-Methods",
                ],
            }
        )
        return response
    elif request.method == "GET":
        response = Response(
            json.dumps(isrecording),
            status=200,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": ["*"]},
        )
        return response
    elif request.method == "POST":
        incoming_data = request.get_data().decode("utf-8")

        try:
            parsed_data = json.loads(incoming_data)
        except:
            parsed_data = ast.literal_eval(incoming_data)

        # Update if Bonnie's recording or not
        isrecording.update(parsed_data)

        # If recording True, turn Purple
        if isrecording["recording"] is True:
            b1 = Blink1()
            b1.fade_to_color(500, "purple")
            b1.close()

        elif isrecording["recording"] is False:
            b1 = Blink1()
            b1.fade_to_color(500, "black")
            b1.close()

        response = Response(
            json.dumps(isrecording),
            status=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json",
            },
        )

        return response


if __name__ == "__main__":
    try:
        app.run(port=9080, host="0.0.0.0")
        turn_led_off()
    except KeyboardInterrupt:
        print("killing the service.")
        quit()
