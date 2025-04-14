import re
import json
import razorpay
from odoo import http
from odoo.http import request
from datetime import datetime, date


class AttendeeRegistration(http.Controller):
    @http.route('/', auth='public', website=True)
    def event_homepage(self, **kwargs):
        """ Render the homepage with the welcome message and upcoming events """
        events = request.env['event.management'].sudo().search([('state', '=', 'upcoming')], limit=6)
        return request.render('Event_management.event_homepage_template', {'events': events})

    @http.route('/events', auth='public', website=True)
    def all_events(self, event_id=None, **kwargs):
        """ Render the events page with a list of all events """
        events = request.env['event.management'].sudo().search([])
        today = date.today()
        return request.render("Event_management.events_page_template", {
            'events': events,
            'today': today,  # Send today's date to the template
        })


    @http.route('/attendee/register', type='http', auth="public", website=True)
    def attendee_registration_form(self, event_id=None, **kwargs):
        events = request.env['event.management'].sudo().search([]) #fetching all the events
        selected_event = None
        ticket_types = []
        ticket_price = 0.0
        # Get the selected event if 'event_id' is provided
        if event_id:
            selected_event = request.env['event.management'].sudo().browse(int(event_id)) if event_id else None
            ticket_types = request.env['event.ticket.type'].sudo().search([('event_id', '=', int(event_id))])
            ticket_price = ticket_types[0].price if ticket_types else 0.0
        return request.render('Event_management.attendee_registration_template', {
            'events': events,
            'selected_event': selected_event,
            'ticket_types': ticket_types,
            'ticket_price': ticket_price,
        })

    class AttendeeRegistration(http.Controller):

        @http.route('/attendee/submit', type='http', auth="public", methods=['POST'], website=True)
        def attendee_registration_submit(self, **post):
            # Extract data
            name = post.get('name')
            email = post.get('email')
            phone = post.get('phone')
            event_id = post.get('event_id')
            ticket_type_id = post.get('ticket_type_id')

            # Validate Email with Regex
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, email):
                events = request.env['event.management'].sudo().search([])
                return request.render('Event_management.attendee_registration_template', {
                    'error': "Invalid email format! Please enter a valid email address.",
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'events': events,
                })

            # Ensure event_id is valid
            event = request.env['event.management'].sudo().browse(int(event_id)) if event_id else None
            if not event or not event.exists():
                return request.render('Event_management.attendee_registration_template', {
                    'error': "Selected event is invalid. Please choose a valid event.",
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'events': request.env['event.management'].sudo().search([]),
                })
                # **Validation: Prevent registration for completed events**
            today_date = datetime.today().date()
            event_date = event.event_date  # Assuming date field exists in event.management
            if event_date and event_date < today_date:
                return request.render('Event_management.attendee_registration_template', {
                    'error': "Registration is closed! This event has already been completed.",
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'events': request.env['event.management'].sudo().search([]),
                })

                # Check if attendee with same email and name already registered for the same event
            existing_attendee = request.env['event.attendee'].sudo().search([
                ('email', '=', email),
                ('name', '=', name),
                ('event_id', '=', int(event_id))
            ], limit=1)

            if existing_attendee:
                return request.render('Event_management.attendee_registration_template', {
                    'error': f"Attendee {name} ({email}) is already registered for this event.",
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'events': request.env['event.management'].sudo().search([]),
                })
            # Create an attendee record in Odoo
            attendee = request.env['event.attendee'].sudo().create({
                'name': name,
                'email': email,
                'phone': phone,
                'event_id': event_id,
            })

            # Send Email Confirmation
            template = request.env.ref('Event_management.email_template_attendee_confirmation')
            if template:
                template.sudo().send_mail(attendee.id, force_send=True)

            # Render success message
            return request.render('Event_management.attendee_registration_template', {
                'success': f"Hurray! {name} registered successfully!",
                'events': request.env['event.management'].sudo().search([]),

            })
