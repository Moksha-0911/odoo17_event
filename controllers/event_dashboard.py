from odoo import http
from odoo.http import request

class EventDashboard(http.Controller):

    @http.route('/event/dashboard', type='http', auth="user", website=True)
    def event_dashboard(self):
        events = request.env['event.management'].sudo().search([])  # Fetching all the events


        event_data = []
        for event in events:
            event_data.append({
                'name': event.name,
                'event_date': event.event_date,
                'attendee_count': request.env['event.attendee'].sudo().search_count([('event_id', '=', event.id)])
            })

        return request.render('Event_management.event_dashboard_template', {
            'events': event_data,
            'total_events': len(events),
            'total_attendees': request.env['event.attendee'].sudo().search_count([]),
        })



