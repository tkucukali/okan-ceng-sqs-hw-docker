import os
import random
from flask import Flask, jsonify, request

app = Flask(__name__)

# Getting the author name from environment variables (HW requirement)
# Default is Tolgahan if not provided in docker run
author_name = os.environ.get("AUTHOR_NAME", "Tolgahan")

# Just some random tech facts for the api
cool_facts = [
    "Docker was released in 2013.",
    "Containers are not VMs, they share the OS kernel instead of virtualizing hardware.",
    "Python is named after Monty Python, not the snake! (I didn't know this)",
    "The first computer bug was an actual real bug (a moth)."
]

# 1. Health check endpoint (Required by homework)
@app.route('/health')
def health_check():
    return jsonify({"status": "ok", "message": "App is running smoothly."})

# 2. Fact endpoint: returns a random fact
@app.route('/fact')
def get_random_fact():
    selected_fact = random.choice(cool_facts)
    return jsonify({
        "provided_by": author_name,
        "fact": selected_fact
    })

# 3. Greet endpoint: takes a query parameter (e.g. /greet?name=Ahmet)
@app.route('/greet')
def greet_user():
    # If no name is provided, use "Guest"
    user_name = request.args.get("name", "Guest")
    return jsonify({
        "message": f"Hello {user_name}! Welcome to {author_name}'s API."
    })

# 4. Stats endpoint: shows how many facts we have
@app.route('/stats')
def get_stats():
    return jsonify({
        "author": author_name,
        "total_facts_available": len(cool_facts)
    })

if __name__ == "__main__":
    # Use port 8080 as default or read from env
    app_port = int(os.environ.get("PORT", 8080))
    print(f"Starting the Fact API on port {app_port}...")
    app.run(host="0.0.0.0", port=app_port)