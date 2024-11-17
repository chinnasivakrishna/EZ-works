import os
from flask import Flask, request, jsonify, send_file
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_mail import Mail, Message
from itsdangerous import URLSafeSerializer
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import magic
import dns.resolver  # Ensure `dnspython` is installed

# Update DNS resolver (optional, if local DNS issues are suspected)
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']  # Use Google's DNS

# App setup
app = Flask(__name__)
api = Api(app)
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # Replace with a strong secret key
app.config["UPLOAD_FOLDER"] = "./uploads"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "chinnasivakrishna2003@gmail.com"  # Replace with your email
app.config["MAIL_PASSWORD"] = "qkjl voce dskw gfru"  # Replace with your password

jwt = JWTManager(app)
mail = Mail(app)
serializer = URLSafeSerializer("secret-key")  # Replace with a strong secret key

# MongoDB setup (Updated for compatibility)
uri = "mongodb+srv://chinnasivakrishna2003:siva@cluster0.u7gjmpo.mongodb.net/file_sharing_system?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["file_sharing_system"]
users_collection = db["users"]
files_collection = db["files"]

# Allowed file types
ALLOWED_EXTENSIONS = {"pptx", "docx", "xlsx"}

@app.route('/')
def home():
    return "Welcome to the File Sharing API!"

# Helper functions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def send_verification_email(email, token):
    link = f"https://ez-works-gmne.onrender.com/verify-email/{token}"
    msg = Message("Verify Your Email", sender="your-email@gmail.com", recipients=[email])
    msg.body = f"Click the link to verify your email: {link}"
    mail.send(msg)


# Resources
class SignUp(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"message": "Email and password are required"}, 400

        if users_collection.find_one({"email": email}):
            return {"message": "Email already exists"}, 400

        token = serializer.dumps(email)
        users_collection.insert_one({"email": email, "password": password, "verified": False})
        send_verification_email(email, token)

        return {"message": "User created. Please verify your email."}, 201


class VerifyEmail(Resource):
    def get(self, token):
        try:
            email = serializer.loads(token)
            user = users_collection.find_one({"email": email})

            if not user:
                return {"message": "Invalid token or user not found."}, 400

            users_collection.update_one({"email": email}, {"$set": {"verified": True}})
            return {"message": "Email verified successfully."}, 200
        except Exception as e:
            return {"message": "Invalid or expired token."}, 400


class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = users_collection.find_one({"email": email, "password": password})

        if not user:
            return {"message": "Invalid credentials"}, 401

        if not user.get("verified"):
            return {"message": "Email not verified"}, 401

        access_token = create_access_token(identity=email)
        return {"access_token": access_token}, 200


class UploadFile(Resource):
    @jwt_required()
    def post(self):
        user_email = get_jwt_identity()
        user = users_collection.find_one({"email": user_email})

        if not user or not user.get("is_ops_user", False):
            return {"message": "Unauthorized: Only Ops Users can upload files."}, 403

        if "file" not in request.files:
            return {"message": "No file provided"}, 400

        file = request.files["file"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            files_collection.insert_one({"filename": filename, "uploader": user_email})
            return {"message": "File uploaded successfully"}, 201

        return {"message": "Invalid file type. Only pptx, docx, and xlsx are allowed."}, 400


class ListFiles(Resource):
    @jwt_required()
    def get(self):
        user_email = get_jwt_identity()
        files = list(files_collection.find({}, {"_id": 0, "filename": 1}))
        return {"files": [file["filename"] for file in files]}, 200


class DownloadFile(Resource):
    @jwt_required()
    def get(self, filename):
        user_email = get_jwt_identity()
        file = files_collection.find_one({"filename": filename})

        if not file:
            return {"message": "File not found"}, 404

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        if not os.path.exists(file_path):
            return {"message": "File not found on server"}, 404

        # Generate token for download
        download_url = serializer.dumps({"filename": filename, "user_email": user_email})
        return {"download_link": f"https://ez-works-gmne.onrender.com/downloadfile/{download_url}"}, 200


class ServeFile(Resource):
    def get(self, token):
        try:
            # Decode the token
            data = serializer.loads(token)
            filename = data.get("filename")
            user_email = data.get("user_email")

            # Debugging output
            print(f"Decoded token: filename={filename}, user_email={user_email}")

            # Validate filename and user_email
            if not filename:
                return {"message": "Invalid file in token"}, 400
            if not user_email:
                return {"message": "Invalid user in token"}, 400

            # Construct file path
            file_path = os.path.abspath(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            print(f"Absolute file path: {file_path}")

            # Check if file exists at the specified path
            if not os.path.exists(file_path):
                return {"message": f"File '{filename}' not found on the server."}, 404

            return send_file(file_path, as_attachment=True)

        except Exception as e:
            print(f"Error during file download: {e}")
            return {"message": "Invalid or expired token"}, 400


# API Routes
api.add_resource(SignUp, "/signup")
api.add_resource(VerifyEmail, "/verify-email/<string:token>")
api.add_resource(Login, "/login")
api.add_resource(UploadFile, "/upload")
api.add_resource(ListFiles, "/list-files")
api.add_resource(DownloadFile, "/download/<string:filename>")
api.add_resource(ServeFile, "/downloadfile/<string:token>")

# Create uploads folder if not exists
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
