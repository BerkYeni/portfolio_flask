from app import app, db
from app.models import Project, Skill, ContactInfo, ContactMessage

@app.before_request
def create_tables():
    db.create_all()
    app.logger.info("Database tables created (if they didn't exist)")

if __name__ == '__main__':
    import os
    if os.environ.get('FLASK_ENV') == 'production':
        from waitress import serve
        app.logger.info("Starting the application in production mode with Waitress")
        serve(app, host="0.0.0.0", port=8080)
    else:
        app.logger.info("Starting the application in development mode")
        app.run(debug=True)