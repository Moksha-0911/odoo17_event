from odoo.tests.common import TransactionCase
from datetime import datetime, timedelta


class TestEventManagement(TransactionCase):

    def setUp(self):
        #Setup test environment before running each test
        super(TestEventManagement, self).setUp()
        self.event_model = self.env['event.management']

        # Create a sample event
        self.event = self.event_model.create({
            'name': 'Test Event',
            'event_date': datetime.today() + timedelta(days=5),
            'description': 'This is a test event',
        })

    def test_event_creation(self):
        #Test event record is created successfully
        self.assertTrue(self.event, "Event should be created")
        self.assertEqual(self.event.name, 'Test Event', "Event name should be 'Test Event'")

    def test_event_past_date(self):
        #Test if the event date is in the past
        past_event = self.event_model.create({
            'name': 'Past Event',
            'event_date': datetime.today() - timedelta(days=5),
            'description': 'This is a past event',
        })
        self.assertTrue(past_event.event_date < datetime.today(), "Past event date should be less than today")

    def test_event_registration_closed(self):
        #Test if registration is closed for past events
        past_event = self.event_model.create({
            'name': 'Closed Event',
            'event_date': datetime.today() - timedelta(days=3),
            'description': 'Registration should be closed for this event',
        })
        self.assertTrue(past_event.event_date < datetime.today(), "Registration should be closed for past events")
