from app import app, db, Event, EventForm, login_manager, User
from datetime import datetime, date, time
import os

# Remove SocketIO dependencies for testing
app.config['TESTING'] = True

# Remove imports that cause issues
@app.route('/events/test', methods=['GET', 'POST'])
def test_events():
    form = EventForm()
    
    if form.validate_on_submit():
        try:
            # Combine date and time
            event_date = form.date.data
            event_time = form.time.data if form.time.data else time(0, 0)
            event_datetime = datetime.combine(event_date, event_time)
            
            # Create event
            event = Event(
                title=form.title.data,
                description=form.description.data,
                event_date=event_datetime,
                event_type=form.event_type.data,
                location=form.location.data,
                created_by=1  # Admin user
            )
            
            db.session.add(event)
            db.session.commit()
            
            return f"SUCCESS: Event '{event.title}' created successfully!"
            
        except Exception as e:
            db.session.rollback()
            return f"ERROR: {str(e)}"
    
    errors = []
    if form.errors:
        for field, field_errors in form.errors.items():
            for error in field_errors:
                errors.append(f"{field}: {error}")
    
    if errors:
        return f"FORM ERRORS: {', '.join(errors)}"
    
    return "Form not validated - check if all required fields are filled"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)