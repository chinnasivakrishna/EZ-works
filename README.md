
---

# File Sharing API with Authentication

This Flask-based File Sharing API allows users to upload, list, and download files, with secure JWT-based authentication. It also includes email verification for user signup. This project uses MongoDB for data storage, Flask-JWT-Extended for authentication, Flask-Mail for email services, and Python's `werkzeug` for file handling.

---

## Features

- **User Sign-Up and Email Verification**: Users can sign up and receive a verification email with a token to verify their email address.
- **Login**: Users can log in after email verification to receive a JWT (JSON Web Token) for secure access.
- **File Upload**: Only users with appropriate permissions (Ops Users) can upload files.
- **File List**: Users can view the list of files available on the server.
- **File Download**: Authenticated users can download files using a secure URL generated for each file.
- **File Type Restrictions**: Only `.pptx`, `.docx`, and `.xlsx` file types are allowed for upload.

---

## How It Works

### 1. **Setup**

- **Flask**: Web framework used to build the API.
- **MongoDB**: Stores user and file data.
- **JWT (JSON Web Token)**: Used for securing API endpoints.
- **Flask-Mail**: Sends verification emails after sign-up.

### 2. **User Signup and Email Verification**
- **POST `/signup`**: Allows users to sign up by providing their email and password. An email verification link is sent to the user's email address.
- **GET `/verify-email/<token>`**: Verifies the user's email by decoding the token sent in the email.

### 3. **Login**
- **POST `/login`**: Users can log in with their email and password, and get a JWT if the credentials are valid and the email is verified.

### 4. **File Operations**
- **POST `/upload`**: Authenticated Ops Users can upload files. Only `.pptx`, `.docx`, and `.xlsx` files are allowed.
- **GET `/list-files`**: Authenticated users can get the list of uploaded files.
- **GET `/download/<filename>`**: Returns a link to download the specified file.
- **GET `/downloadfile/<token>`**: Downloads the file if the token is valid.

---

## Endpoints

### 1. **User Management**
- **POST `/signup`**: Creates a new user. Requires email and password in the request body.
- **GET `/verify-email/<token>`**: Verifies the user's email using the token sent via email.
- **POST `/login`**: Authenticates the user and returns an access token.

### 2. **File Management**
- **POST `/upload`**: Uploads a file (JWT required).
- **GET `/list-files`**: Lists all uploaded files (JWT required).
- **GET `/download/<filename>`**: Provides a download link for the file (JWT required).
- **GET `/downloadfile/<token>`**: Serves the file for download using a token.

---

## Deployment

This app is deployed at:

**[Deployed API](https://ez-works-gmne.onrender.com)**

You can access the API and perform requests using the provided Postman collection or by interacting directly via HTTP requests.

---

## Postman Collection

You can import the following Postman collection to test the API:

**[Postman Collection](https://web.postman.co/workspace/My-Workspace~d1061c07-65cf-4949-82b2-9a2f8e064dd4/collection/31655496-40eb47a3-0dc9-45af-a163-89131a38fcde?action=share&source=copy-link&creator=31655496&active-environment=96b4c8e7-5040-474c-9c58-6304e03eccc7)**  

---

## Requirements

To run the application locally, ensure you have the following dependencies installed:

### `requirements.txt`

```txt
Flask==2.3.3
Flask-RESTful==0.3.9
Flask-JWT-Extended==4.6.0
Flask-Mail==0.9.1
pymongo==4.5.0
python-magic==0.4.24
itsdangerous==2.0.1
werkzeug==2.3.5
dnspython==2.2.1
```

---

## Installation & Setup

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/your-repository/file-sharing-api.git
cd file-sharing-api
```

### Step 2: Install Dependencies

Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### Step 3: Set Up MongoDB

Make sure you have MongoDB set up and configured. If you're using MongoDB Atlas, ensure the URI in the `app.py` is correctly configured with your credentials.

### Step 4: Run the Application

Start the Flask app:

```bash
python app.py
```

The app will be running on `http://localhost:5000`.

---

## Configuration

### 1. **Email Configuration**

Make sure to replace the following in `app.py` with your actual email and SMTP settings:

```python
app.config["MAIL_USERNAME"] = "your-email@gmail.com"
app.config["MAIL_PASSWORD"] = "your-email-password"
```

### 2. **JWT Configuration**

Set a secure JWT secret key:

```python
app.config["JWT_SECRET_KEY"] = "your-jwt-secret-key"
```

### 3. **File Upload Directory**

By default, files are uploaded to the `./uploads` directory. You can change this in the configuration.

---

## Error Handling

If something goes wrong, the API will return a descriptive message. For example:
- `400`: Bad request (e.g., missing fields or invalid token).
- `401`: Unauthorized (e.g., invalid credentials or email not verified).
- `404`: Not found (e.g., file not found).
- `500`: Internal server error (e.g., server or database issues).

---

## Security Notes

- The app uses JWT tokens for secure authentication.
- All file uploads are validated to ensure only `.pptx`, `.docx`, and `.xlsx` files are allowed.
- The app only allows users with specific roles (Ops Users) to upload files.

---
