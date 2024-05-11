from flask import Flask, jsonify
from celery import Celery

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/')
def hello():
    return "Hello, World!"

@celery.task
def add_together(a, b):
    return a + b

@celery.task
def send_email(email_address, message):
    # Simulate sending an email
    print(f"Sending email to {email_address} with message: {message}")
    return f"Email sent to {email_address}"

@celery.task
def long_computation(number):
    # Simulate a long computation by calculating factorial
    result = 1
    for i in range(1, number + 1):
        result *= i
    return result

@app.route('/add/<int:a>/<int:b>')
def add(a, b):
    result = add_together.delay(a, b)
    return jsonify({"result": result.get()})

@app.route('/send_email/<email>')
def email(email):
    result = send_email.delay(email, "Hello from our app!")
    return jsonify({"result": "Email is being sent..."})

@app.route('/compute/<int:number>')
def compute(number):
    result = long_computation.delay(number)
    return jsonify({"result": "Computation started. Check back for results later."})

if __name__ == "__main__":
    app.run(debug=True)
