
# **TransactShield Authentication**

TransactShield is a secure authentication system designed to streamline user registration, login, and profile management. Built with modern technologies, it ensures a seamless and user-friendly experience.

---

## **Table of Contents**
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Authentication Flow](#authentication-flow)
- [Setup Instructions](#setup-instructions)
- [Hosted Links](#hosted-links)

---

## **Features**
- User Registration with secure password hashing.
- Login functionality with JWT token-based authentication.
- Protected profile route accessible only by authenticated users.
- Responsive UI designed with Tailwind CSS.

---

## **Tech Stack**
- **Backend**: FastAPI, PostgreSQL, SQLAlchemy
- **Authentication**: JSON Web Tokens (JWT)
- **Hosting**: Render (Backend)

---

## **Authentication Flow**

1. **Registration**:
   - The user submits a username, email, and password.
   - Passwords are securely hashed before storage in the database.
   - A new user record is created.

2. **Login**:
   - The user provides email and password.
   - The backend verifies the credentials and generates a JWT token upon success.
   - The token is stored in a cookie for secure communication.

3. **Protected Profile Route**:
   - The user must be authenticated to access the profile page.
   - The frontend sends the JWT token to the backend for verification.
   - Upon verification, the user's profile data is returned.

---

## **Setup Instructions**

### **Backend Setup**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/transactshield-backend.git
   cd transactshield-backend
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the project root with the following contents:
     ```
     DATABASE_URL=postgresql://username:password@localhost:5432/auth_app
     SECRET_KEY=your-secret-key
     ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     ```

5. **Apply Migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Start the Server**:
   ```bash
   uvicorn app.main:app --reload
   ```
   - The backend will be running at `http://127.0.0.1:8000`.

---


## **Hosted Links**

- **Backend**: [https://your-backend-link.com](https://your-backend-link.com)

---

