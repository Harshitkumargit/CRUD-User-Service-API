from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from app.schemas import UserCreate, UserUpdate, UserResponse
from app.crud import create_user, get_user, update_user, delete_user, get_all_users
from app.database import init_db, get_db
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="User Service API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database
init_db()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    logger.info("Serving root endpoint")
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>User Service API</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @keyframes fadeInDown {
                0% { opacity: 0; transform: translateY(-20px); }
                100% { opacity: 1; transform: translateY(0); }
            }
            @keyframes slideInUp {
                0% { opacity: 0; transform: translateY(20px); }
                100% { opacity: 1; transform: translateY(0); }
            }
            @keyframes slideInLeft {
                0% { opacity: 0; transform: translateX(-20px); }
                100% { opacity: 1; transform: translateX(0); }
            }
            .animate-fadeInDown {
                animation: fadeInDown 0.8s ease-out;
            }
            .animate-slideInUp {
                animation: slideInUp 0.8s ease-out;
            }
            .animate-slideInLeft {
                animation: slideInLeft 0.8s ease-out both;
            }
            .card-hover:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
            }
            html {
                scroll-behavior: smooth;
            }
        </style>
    </head>
    <body class="bg-gray-50 font-sans antialiased">
        <div class="min-h-screen flex flex-col">
            <header class="bg-gradient-to-r from-blue-700 to-indigo-600 text-white py-12">
                <div class="container mx-auto px-4 text-center animate-fadeInDown">
                    <h1 class="text-5xl font-extrabold mb-4">User Service API</h1>
                    <p class="text-xl max-w-2xl mx-auto">
                        A powerful, scalable, and secure API for managing user data with ease.
                    </p>
                    <a href="/manage-users" class="mt-6 inline-block bg-white text-blue-700 px-8 py-4 rounded-full font-semibold text-lg hover:bg-blue-100 transition duration-300">
                        Manage Users
                    </a>
                    <a href="/docs" class="mt-4 ml-4 inline-block bg-transparent border-2 border-white text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-white hover:text-blue-700 transition duration-300">
                        API Documentation
                    </a>
                </div>
            </header>
            <main class="container mx-auto px-4 py-16 flex-grow">
                <section class="text-center mb-16 animate-slideInUp">
                    <h2 class="text-3xl font-bold text-gray-800 mb-4">Why User Service API?</h2>
                    <p class="text-lg text-gray-600 max-w-3xl mx-auto">
                        Built with FastAPI and SQLAlchemy, our API offers robust endpoints for creating, reading, updating, and deleting user information, all backed by a reliable SQLite database.
                    </p>
                </section>
                <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
                    <div class="bg-white shadow-lg rounded-xl p-6 animate-slideInLeft card-hover transition duration-300" style="animation-delay: 0.1s;">
                        <h3 class="text-xl font-semibold text-gray-800 mb-3">Create User</h3>
                        <p class="text-gray-600 mb-4">Easily add new users with email, name, and optional age fields.</p>
                        <code class="block bg-gray-100 p-3 rounded-lg text-sm font-mono">POST /users/</code>
                    </div>
                    <div class="bg-white shadow-lg rounded-xl p-6 animate-slideInLeft card-hover transition duration-300" style="animation-delay: 0.2s;">
                        <h3 class="text-xl font-semibold text-gray-800 mb-3">Read User</h3>
                        <p class="text-gray-600 mb-4">Retrieve detailed user information by their unique ID.</p>
                        <code class="block bg-gray-100 p-3 rounded-lg text-sm font-mono">GET /users/{user_id}</code>
                    </div>
                    <div class="bg-white shadow-lg rounded-xl p-6 animate-slideInLeft card-hover transition duration-300" style="animation-delay: 0.3s;">
                        <h3 class="text-xl font-semibold text-gray-800 mb-3">Update User</h3>
                        <p class="text-gray-600 mb-4">Modify existing user details with flexible updates.</p>
                        <code class="block bg-gray-100 p-3 rounded-lg text-sm font-mono">PUT /users/{user_id}</code>
                    </div>
                    <div class="bg-white shadow-lg rounded-xl p-6 animate-slideInLeft card-hover transition duration-300" style="animation-delay: 0.4s;">
                        <h3 class="text-xl font-semibold text-gray-800 mb-3">Delete User</h3>
                        <p class="text-gray-600 mb-4">Securely remove users from the database by ID.</p>
                        <code class="block bg-gray-100 p-3 rounded-lg text-sm font-mono">DELETE /users/{user_id}</code>
                    </div>
                </section>
                <section class="text-center animate-slideInUp">
                    <h2 class="text-3xl font-bold text-gray-800 mb-4">Get Started Today</h2>
                    <p class="text-lg text-gray-600 max-w-2xl mx-auto mb-6">
                        Dive into our interactive API documentation or manage users directly with our intuitive interface.
                    </p>
                    <a href="/manage-users" class="inline-block bg-blue-600 text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-blue-700 transition duration-300">
                        Manage Users
                    </a>
                </section>
            </main>
            <footer class="bg-gray-900 text-white py-8">
                <div class="container mx-auto px-4 text-center">
                    <p class="text-sm">© 2025 User Service API. All rights reserved.</p>
                    <p class="mt-2 text-sm">
                        Powered by <a href="https://fastapi.tiangolo.com/" class="underline hover:text-blue-300">FastAPI</a> & <a href="https://www.sqlalchemy.org/" class="underline hover:text-blue-300">SQLAlchemy</a>.
                    </p>
                </div>
            </footer>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/manage-users", response_class=HTMLResponse)
async def manage_users():
    logger.info("Serving manage-users endpoint")
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Manage Users - User Service API</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @keyframes fadeIn {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }
            @keyframes slideInUp {
                0% { opacity: 0; transform: translateY(20px); }
                100% { opacity: 1; transform: translateY(0); }
            }
            .animate-fadeIn {
                animation: fadeIn 0.6s ease-out;
            }
            .animate-slideInUp {
                animation: slideInUp 0.8s ease-out;
            }
            .btn-hover:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }
            .message {
                transition: opacity 0.3s ease-in-out;
            }
            html {
                scroll-behavior: smooth;
            }
        </style>
    </head>
    <body class="bg-gray-50 font-sans antialiased">
        <div class="min-h-screen flex flex-col">
            <header class="bg-gradient-to-r from-blue-700 to-indigo-600 text-white py-12">
                <div class="container mx-auto px-4 text-center animate-fadeIn">
                    <h1 class="text-4xl font-extrabold mb-4">Manage Users</h1>
                    <p class="text-lg max-w-2xl mx-auto">
                        Easily add, delete, or view all users in the system with our intuitive interface.
                    </p>
                    <a href="/" class="mt-4 inline-block bg-transparent border-2 border-white text-white px-6 py-3 rounded-full font-semibold hover:bg-white hover:text-blue-700 transition duration-300">
                        Back to Home
                    </a>
                </div>
            </header>
            <main class="container mx-auto px-4 py-12 flex-grow">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
                    <section class="bg-white shadow-lg rounded-xl p-8 animate-slideInUp">
                        <h2 class="text-2xl font-semibold text-gray-800 mb-6">Add New User</h2>
                        <div id="add-user-message" class="hidden mb-4 p-4 rounded-lg"></div>
                        <div class="space-y-4">
                            <div>
                                <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
                                <input type="email" id="email" name="email" required class="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" placeholder="Enter email">
                            </div>
                            <div>
                                <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
                                <input type="text" id="name" name="name" required class="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" placeholder="Enter name">
                            </div>
                            <div>
                                <label for="age" class="block text-sm font-medium text-gray-700">Age (Optional)</label>
                                <input type="number" id="age" name="age" class="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" placeholder="Enter age">
                            </div>
                            <button onclick="addUser()" class="w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold btn-hover transition duration-300">Add User</button>
                        </div>
                    </section>
                    <section class="bg-white shadow-lg rounded-xl p-8 animate-slideInUp" style="animation-delay: 0.2s;">
                        <h2 class="text-2xl font-semibold text-gray-800 mb-6">Delete User</h2>
                        <div id="delete-user-message" class="hidden mb-4 p-4 rounded-lg"></div>
                        <div class="space-y-4">
                            <div>
                                <label for="user_id" class="block text-sm font-medium text-gray-700">User ID</label>
                                <input type="number" id="user_id" name="user_id" required class="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" placeholder="Enter user ID">
                            </div>
                            <button onclick="deleteUser()" class="w-full bg-red-600 text-white px-6 py-3 rounded-lg font-semibold btn-hover transition duration-300">Delete User</button>
                        </div>
                    </section>
                </div>
                <section class="bg-white shadow-lg rounded-xl p-8 animate-slideInUp" style="animation-delay: 0.4s;">
                    <h2 class="text-2xl font-semibold text-gray-800 mb-6">All Users</h2>
                    <div id="users-message" class="hidden mb-4 p-4 rounded-lg"></div>
                    <button onclick="fetchUsers()" class="mb-6 bg-indigo-600 text-white px-6 py-3 rounded-lg font-semibold btn-hover transition duration-300">Refresh User List</button>
                    <div class="overflow-x-auto">
                        <table id="users-table" class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Age</th>
                                </tr>
                            </thead>
                            <tbody id="users-table-body" class="bg-white divide-y divide-gray-200">
                                <!-- Users will be populated here -->
                            </tbody>
                        </table>
                    </div>
                </section>
            </main>
            <footer class="bg-gray-900 text-white py-8">
                <div class="container mx-auto px-4 text-center">
                    <p class="text-sm">© 2025 User Service API. All rights reserved.</p>
                    <p class="mt-2 text-sm">
                        Powered by <a href="https://fastapi.tiangolo.com/" class="underline hover:text-blue-300">FastAPI</a> & <a href="https://www.sqlalchemy.org/" class="underline hover:text-blue-300">SQLAlchemy</a>.
                    </p>
                </div>
            </footer>
        </div>
        <script>
            async function addUser() {
                const messageDiv = document.getElementById('add-user-message');
                messageDiv.classList.add('hidden');
                messageDiv.classList.remove('bg-green-100', 'text-green-700', 'bg-red-100', 'text-red-700');

                const email = document.getElementById('email').value;
                const name = document.getElementById('name').value;
                const age = document.getElementById('age').value || null;

                try {
                    const response = await fetch('/users/', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email, name, age: age ? parseInt(age) : null })
                    });
                    if (!response.ok) {
                        const text = await response.text();
                        console.error('Add User Error Response:', text);
                        let errorDetail;
                        try {
                            errorDetail = JSON.parse(text).detail;
                        } catch {
                            errorDetail = text || 'Failed to create user';
                        }
                        throw new Error(errorDetail);
                    }
                    const data = await response.json();
                    messageDiv.classList.remove('hidden');
                    messageDiv.classList.add('bg-green-100', 'text-green-700');
                    messageDiv.textContent = `User created successfully! ID: ${data.id}`;
                    document.getElementById('email').value = '';
                    document.getElementById('name').value = '';
                    document.getElementById('age').value = '';
                    fetchUsers(); // Refresh user list
                } catch (error) {
                    messageDiv.classList.remove('hidden');
                    messageDiv.classList.add('bg-red-100', 'text-red-700');
                    messageDiv.textContent = error.message;
                }
            }

            async function deleteUser() {
                const messageDiv = document.getElementById('delete-user-message');
                messageDiv.classList.add('hidden');
                messageDiv.classList.remove('bg-green-100', 'text-green-700', 'bg-red-100', 'text-red-700');

                const user_id = document.getElementById('user_id').value;

                try {
                    const response = await fetch(`/users/${user_id}`, {
                        method: 'DELETE',
                        headers: { 'Content-Type': 'application/json' }
                    });
                    if (!response.ok) {
                        const text = await response.text();
                        console.error('Delete User Error Response:', text);
                        let errorDetail;
                        try {
                            errorDetail = JSON.parse(text).detail;
                        } catch {
                            errorDetail = text || 'Failed to delete user';
                        }
                        throw new Error(errorDetail);
                    }
                    const data = await response.json();
                    messageDiv.classList.remove('hidden');
                    messageDiv.classList.add('bg-green-100', 'text-green-700');
                    messageDiv.textContent = data.message;
                    document.getElementById('user_id').value = '';
                    fetchUsers(); // Refresh user list
                } catch (error) {
                    messageDiv.classList.remove('hidden');
                    messageDiv.classList.add('bg-red-100', 'text-red-700');
                    messageDiv.textContent = error.message;
                }
            }

            async function fetchUsers() {
                const messageDiv = document.getElementById('users-message');
                const tableBody = document.getElementById('users-table-body');
                messageDiv.classList.add('hidden');
                messageDiv.classList.remove('bg-green-100', 'text-green-700', 'bg-red-100', 'text-red-700');

                try {
                    const response = await fetch('/users/', {
                        method: 'GET',
                        headers: { 'Content-Type': 'application/json' }
                    });
                    if (!response.ok) {
                        const text = await response.text();
                        console.error('Fetch Users Error Response:', text);
                        let errorDetail;
                        try {
                            errorDetail = JSON.parse(text).detail;
                        } catch {
                            errorDetail = text || 'Failed to fetch users';
                        }
                        throw new Error(errorDetail);
                    }
                    const data = await response.json();
                    tableBody.innerHTML = '';
                    if (data.length === 0) {
                        tableBody.innerHTML = '<tr><td colspan="4" class="px-6 py-4 text-center text-gray-500">No users found</td></tr>';
                    } else {
                        data.forEach(user => {
                            const row = document.createElement('tr');
                            row.innerHTML = `
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${user.id}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${user.email}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${user.name}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${user.age || '-'}</td>
                            `;
                            tableBody.appendChild(row);
                        });
                    }
                } catch (error) {
                    messageDiv.classList.remove('hidden');
                    messageDiv.classList.add('bg-red-100', 'text-red-700');
                    messageDiv.textContent = error.message;
                }
            }

            document.addEventListener('DOMContentLoaded', fetchUsers);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/users/", response_model=List[UserResponse])
async def get_all_users_endpoint(db: Session = Depends(get_db)):
    try:
        users = get_all_users(db)
        logger.info(f"Retrieved {len(users)} users from endpoint")
        return users
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_all_users_endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve users: {str(e)}"
        )

@app.post("/users/", response_model=UserResponse)
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = create_user(user, db)
        if not db_user:
            raise HTTPException(status_code=400, detail="Email already exists")
        logger.info(f"Created user with ID: {db_user.id}")
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_user_endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create user: {str(e)}"
        )

@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    try:
        user = get_user(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        logger.info(f"Retrieved user with ID: {user_id}")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in read_user_endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve user: {str(e)}"
        )

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        updated_user = update_user(user_id, user, db)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        logger.info(f"Updated user with ID: {user_id}")
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_user_endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update user: {str(e)}"
        )

@app.delete("/users/{user_id}")
async def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    try:
        if not delete_user(user_id, db):
            raise HTTPException(status_code=404, detail="User not found")
        logger.info(f"Deleted user with ID: {user_id}")
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_user_endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete user: {str(e)}"
        )