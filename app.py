from flask import Flask,request,jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime
import os
import razorpay
import hmac
import hashlib

load_dotenv()

app=Flask(__name__)
CORS(app)

razorpay_client = razorpay.Client(auth=(
    os.getenv("keyId"),
    os.getenv("KeySecret")
)
)

@app.route("/payment",methods=["POST"])
def createOrder():
    try:
        data = request.get_json()
        amount= int(data["amount"])
        options = {
            "amount":amount*100,
            "currency":"INR",
            "receipt":f"receipt_{datetime.now().strftime("%d%m%Y%H%M%S")}",
            "payment_capture":1
        }
        order = razorpay_client.order.create(options)
        return jsonify(order)
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route("/verify",methods=["POST"])
def verify():
    data= request.get_json()
    razorpay_payment_id= data["razorpay_payment_id"]
    razorpay_order_id= data["razorpay_order_id"]
    razorpay_signature= data["razorpay_signature"]

    body= f"{razorpay_order_id}|{razorpay_payment_id}"
    expectedSignature = hmac.new(
        bytes(os.getenv("KeySecret"),'utf-8'),
        bytes(body,'utf-8'),
        hashlib.sha256
    ).hexdigest()

    if expectedSignature == razorpay_signature:
        return jsonify({"message":"Payment Successful !","expectedSignature":expectedSignature})
    else:
        return jsonify({"message":"Payment Failed.","expectedSignature":expectedSignature})



if __name__ == "__main__":
    app.run(port=os.getenv("PORT"),debug=True)