"""
Main application entry point
"""
import sys
from flask import Flask
from core.permissions import check_runtime_privilege
from config.settings import FLASK_HOST, FLASK_PORT, FLASK_DEBUG
from api.routes import create_routes


def create_app():
    """Create Flask application"""
    app = Flask(__name__)

    # Register routes
    create_routes(app)

    return app


def main():
    """Main function"""
    # Check runtime permissions
    privilege_info = check_runtime_privilege()

    # Display privilege information
    print("=" * 50)
    print("  Multi-AI Environment Config Manager")
    print("=" * 50)
    print(f"  Server: http://localhost:{FLASK_PORT}")
    print(f"  Mode: {'Development' if FLASK_DEBUG else 'Production'}")
    print(f"  Privilege Level: {privilege_info['level']}")
    print(f"  Can Modify Environment: {'Yes' if privilege_info['can_modify_env'] else 'No'}")
    print("=" * 50)

    # Display recommendations
    for recommendation in privilege_info['recommendations']:
        if recommendation['type'] == 'error':
            print(f"  ERROR: {recommendation['message']}")
        elif recommendation['type'] == 'warning':
            print(f"  WARNING: {recommendation['message']}")
        elif recommendation['type'] == 'success':
            print(f"  SUCCESS: {recommendation['message']}")
    print("=" * 50)
    print("  Press Ctrl+C to stop service")
    print()

    # Create Flask application
    app = create_app()

    # Add privilege info to app context for API access
    app.config['PRIVILEGE_INFO'] = privilege_info

    # Start Flask application
    try:
        app.run(
            host=FLASK_HOST,
            port=FLASK_PORT,
            debug=FLASK_DEBUG
        )
    except KeyboardInterrupt:
        print("\nService stopped")


if __name__ == '__main__':
    main()