# Project Documentation

## Demo
![image](https://github.com/user-attachments/assets/4e101309-ac22-4a3f-9e0d-92d334c76b58)
![image](https://github.com/user-attachments/assets/d378b37e-b207-4088-9219-2d9d4cfe4048)
![image](https://github.com/user-attachments/assets/43d74c2b-5150-40a9-88c0-461f64a6894c)

https://github.com/user-attachments/assets/185a64fe-4a7a-45d0-b912-f2e03a4a4fef

## Overview

This project consists of a backend service for data analysis and a frontend application for visualization. The backend is built with Flask, and the frontend is a Svelte application using TailwindCSS and DaisyUI for styling.

## Prerequisites

- Python 3.8 or higher
- Node.js 18.x or higher
- `pip` for Python package management
- `npm` or `yarn` for Node.js package management

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/vansh-goel/Water-Quality-Analysis/
cd Water-Quality-Analysis/
```

# Project Setup Instructions

## 3. Backend Setup

### a. Install Backend Dependencies

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Install the dependencies**:
   Make sure you have `pip` installed. Then, run:
   ```bash
   pip install -r requirements.txt
   ```

### b. Start the Backend Server

1. **Run the Flask application**:
   ```bash
   flask run
   ```
   By default, the backend server will start on `http://localhost:5000`. You can change this by setting the `FLASK_RUN_PORT` environment variable.

## 4. Frontend Setup

### a. Install Frontend Dependencies

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install the dependencies**:
   You can use either `npm` or `yarn`.
   
   Using `npm`:
   ```bash
   npm install
   ```
   
   Using `yarn`:
   ```bash
   yarn install
   ```

### b. Start the Frontend Development Server

1. **Run the development server**:
   
   Using `npm`:
   ```bash
   npm run dev
   ```
   
   Using `yarn`:
   ```bash
   yarn dev
   ```
   By default, the frontend development server will start on `http://localhost:3000`.

## 5. Access the Application

* **Frontend**: Open `http://localhost:3000` in your web browser.
* **Backend API**: Access the API at `http://localhost:5000`.
