from flask import Flask, render_template, jsonify
from PaymentFiservAPI import PaymentService

app = Flask(__name__)

@app.route('/make_payment', methods=['GET', 'POST'])
def make_payment():
    if request.method == 'POST':
        try:
            # Create an instance of the PaymentService class
            payment_service = PaymentService()

            # Make the payment request
            payment_service.make_payment_request()

            return jsonify({"status": "success", "message": "Payment request sent successfully"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        return render_template('make_payment.html')

if __name__ == '__main__':
    app.run(debug=True)