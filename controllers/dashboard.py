from odoo import http
from odoo.http import request

class EventDashboard(http.Controller):

    @http.route('/dashboard', type='http', auth='user', website=True)
    def dashboard(self, **kwargs):
        events = request.env['event.management'].sudo().search([], order="event_date desc")  # Fetch events
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        #filters data of events on the basis of start and end date
        if start_date and end_date:
            events = events.filtered(lambda e: start_date <= e.event_date.strftime('%Y-%m-%d') <= end_date)

        event_data = [{
            'name': event.name,
            'event_date': event.event_date.strftime('%Y-%m-%d'),
            'attendee_count': len(event.attendee_ids),
        } for event in events]

        values = {
            'total_events': len(events),#displays the length of the events
            'total_attendees': sum(len(event.attendee_ids) for event in events), #displays all the attendees
            'events': event_data,  # fetches all the events from the event.management model
        }


        return request.render('Event_management.dashboard_template', values)



