from flask import render_template, abort, request, flash, redirect, url_for
from app import app, db, mail, cache
from app.models import Project, Skill, ContactInfo, ContactMessage
from app.forms import ContactForm
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from flask_mail import Message  # Add this import

# Remove or comment out these lines as they're already configured in __init__.py
# app.config['MAIL_SERVER'] = 'smtp.example.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'your-email@example.com'
# app.config['MAIL_PASSWORD'] = 'your-email-password'
# app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'

# Remove this line as mail is already initialized in __init__.py
# mail = Mail(app)

current_year = datetime.now().year

@app.route('/')
@cache.cached(timeout=60)  # Cache for 1 minute
def index():
    try:
        projects = Project.query.order_by(Project.created_at.desc()).limit(3).all()
        skills = Skill.query.order_by(Skill.proficiency.desc()).all()
        contact_info = ContactInfo.query.first()
        
        if not projects and not skills:
            app.logger.warning("No projects or skills found")
            # Instead of aborting, we'll render the template with empty lists
            return render_template('index.html', projects=[], skills=[], contact_info=contact_info, current_year=current_year)
        
        return render_template('index.html', projects=projects, skills=skills, contact_info=contact_info, current_year=current_year)
    except SQLAlchemyError as e:
        app.logger.error(f"Database error in index route: {str(e)}")
        abort(500)

@app.route('/projects')
@cache.cached(timeout=60)  # Cache for 1 minute
def projects():
    try:
        page = request.args.get('page', 1, type=int)
        projects = Project.query.order_by(Project.created_at.desc()).paginate(page=page, per_page=6)
        
        if not projects.items and page != 1:
            app.logger.warning(f"No projects found on page {page}")
            abort(404, description="No projects found on this page")
        
        return render_template('projects.html', projects=projects, current_year=current_year)
    except SQLAlchemyError as e:
        app.logger.error(f"Database error in projects route: {str(e)}")
        abort(500)

@app.route('/skills')
@cache.cached(timeout=300)  # Cache for 5 minutes
def skills():
    try:
        skills = Skill.query.order_by(Skill.proficiency.desc()).all()
        
        if not skills:
            app.logger.warning("No skills found")
            # Instead of aborting, we'll render the template with an empty list
            return render_template('skills.html', skills=[], current_year=current_year)
        
        return render_template('skills.html', skills=skills, current_year=current_year)
    except SQLAlchemyError as e:
        app.logger.error(f"Database error in skills route: {str(e)}")
        abort(500)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    try:
        contact_info = ContactInfo.query.first()
        
        if form.validate_on_submit():
            message = ContactMessage(
                name=form.name.data,
                email=form.email.data,
                message=form.message.data
            )
            db.session.add(message)
            db.session.commit()
            
            # Send email
            email_message = Message(
                subject='New Contact Form Submission',
                recipients=[app.config['MAIL_DEFAULT_SENDER']],
                body=f"Name: {form.name.data}\nEmail: {form.email.data}\nMessage: {form.message.data}"
            )
            mail.send(email_message)
            
            app.logger.info(f"New contact message from {form.name.data} ({form.email.data})")
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('contact'))
        
        return render_template('contact.html', contact_info=contact_info, form=form, current_year=current_year)
    except SQLAlchemyError as e:
        app.logger.error(f"Database error in contact route: {str(e)}")
        abort(500)

@app.errorhandler(404)
def not_found_error(error):
    app.logger.warning(f"404 error: {error}")
    return render_template('404.html', error=error, current_year=current_year), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"500 error: {error}")
    db.session.rollback()
    return render_template('500.html', current_year=current_year), 500