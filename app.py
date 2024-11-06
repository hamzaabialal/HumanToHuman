from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)

# Configuring the SQLite database URL (you can configure other databases like MySQL or PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Directory where uploaded files will be stored
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the database
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    front_side_image = db.Column(db.String(120), nullable=True)  # Store the file path
    left_side_image = db.Column(db.String(120), nullable=True)
    right_side_image = db.Column(db.String(120), nullable=True)
    voice_notes = db.Column(db.String(120), nullable=True)  # Store the file path

# Create the database
with app.app_context():
    db.create_all()

# Root route
@app.route('/')
def hello_world():
    return 'Hello World!'

# Register route to handle POST requests
@app.route('/register', methods=['POST'])
def register():
    # Get the data from the POST request (form data)
    username = request.form.get('username')
    email = request.form.get('email')

    # Check if the username and email were provided
    if not username or not email:
        return jsonify({"error": "Username and email are required"}), 400

    # Check if the email already exists in the database
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 409

    # Handle file uploads
    front_image = request.files.get('front_side_image')
    left_image = request.files.get('left_side_image')
    right_image = request.files.get('right_side_image')
    voice_note = request.files.get('voice_notes')

    # Save the files if they exist
    if front_image:
        front_image_path = os.path.join(app.config['UPLOAD_FOLDER'], front_image.filename)
        front_image.save(front_image_path)
    else:
        front_image_path = None

    if left_image:
        left_image_path = os.path.join(app.config['UPLOAD_FOLDER'], left_image.filename)
        left_image.save(left_image_path)
    else:
        left_image_path = None

    if right_image:
        right_image_path = os.path.join(app.config['UPLOAD_FOLDER'], right_image.filename)
        right_image.save(right_image_path)
    else:
        right_image_path = None

    if voice_note:
        voice_note_path = os.path.join(app.config['UPLOAD_FOLDER'], voice_note.filename)
        voice_note.save(voice_note_path)
    else:
        voice_note_path = None

    # Create a new User object
    new_user = User(
        username=username,
        email=email,
        front_side_image=front_image_path,
        left_side_image=left_image_path,
        right_side_image=right_image_path,
        voice_notes=voice_note_path
    )

    # Add the user to the session and commit to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True)
