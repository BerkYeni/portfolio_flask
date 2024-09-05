from app import app, db
from app.models import Project, Skill, ContactInfo

def populate_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Add projects
        projects = [
            Project(title="Portfolio Website", description="A personal portfolio website built with Flask and Tailwind CSS.", project_url="https://github.com/yourusername/portfolio"),
            Project(title="Task Manager", description="A web-based task management application with user authentication.", project_url="https://github.com/yourusername/task-manager"),
            Project(title="Weather App", description="A weather forecast application using a third-party API.", project_url="https://github.com/yourusername/weather-app"),
        ]
        db.session.add_all(projects)

        # Add skills
        skills = [
            Skill(name="Python", proficiency=5),
            Skill(name="Flask", proficiency=4),
            Skill(name="HTML/CSS", proficiency=4),
            Skill(name="JavaScript", proficiency=3),
            Skill(name="SQL", proficiency=3),
        ]
        db.session.add_all(skills)

        # Add contact info
        contact_info = ContactInfo(
            email="your.email@example.com",
            phone="+1 (123) 456-7890",
            linkedin="https://www.linkedin.com/in/yourusername",
            github="https://github.com/yourusername"
        )
        db.session.add(contact_info)

        db.session.commit()
        print("Database populated successfully!")

if __name__ == "__main__":
    populate_database()