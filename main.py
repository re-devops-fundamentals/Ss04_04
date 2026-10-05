"""
DevOps Fundamentals - Session 04 - Exercise 4
Git Ignore & History Amendment
Author: HoQuocKhai
Email: khaiho6040@gmail.com
"""

import os

def load_system_config():
    # Load configuration securely from environment variables instead of hardcoded files
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    return {
        "host": db_host,
        "port": db_port,
        "environment": "production"
    }

def main():
    config = load_system_config()
    print("Application initialized successfully with secure config:")
    print(config)

if __name__ == "__main__":
    main()
