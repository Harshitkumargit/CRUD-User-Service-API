import sqlite3

# Connect to the database
conn = sqlite3.connect('user_service.db')
cursor = conn.cursor()

# Query the users table
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the connection
conn.close()