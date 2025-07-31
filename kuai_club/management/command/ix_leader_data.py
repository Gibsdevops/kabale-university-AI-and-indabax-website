from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Fix leader data and set appropriate end dates for testing'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--create-test-data',
            action='store_true',
            help='Create some test previous leaders',
        )
        parser.add_argument(
            '--update-existing',
            action='store_true',
            help='Update existing leaders with past end dates',
        )
    
    def handle(self, *args, **options):
        if options['create_test_data']:
            self.create_test_data()
        
        if options['update_existing']:
            self.update_existing_leaders()
    
    def create_test_data(self):
        """Create some test previous leaders"""
        from kuai_club.models import Leader  # Replace 'myapp' with your app name
        from datetime import date
        
        test_leaders = [
            {
                'full_name': 'John Doe',
                'position': 'President',
                'category': 'student',
                'year_served': 2023,
                'start_date': date(2023, 1, 1),
                'end_date': date(2023, 12, 31),
                'bio': 'Led the club through major expansion in 2023.',
                'email': 'john.doe@example.com'
            },
            {
                'full_name': 'Jane Smith',
                'position': 'Technical Lead',
                'category': 'student',
                'year_served': 2022,
                'start_date': date(2022, 1, 1),
                'end_date': date(2022, 12, 31),
                'bio': 'Pioneered the AI workshop series.',
                'email': 'jane.smith@example.com'
            },
            {
                'full_name': 'Dr. Alice Johnson',
                'position': 'Faculty Advisor',
                'category': 'faculty',
                'year_served': 2023,
                'start_date': date(2023, 1, 1),
                'end_date': date(2023, 6, 30),
                'bio': 'Provided academic guidance and mentorship.',
                'email': 'alice.johnson@university.edu'
            },
        ]
        
        for leader_data in test_leaders:
            leader, created = Leader.objects.get_or_create(
                full_name=leader_data['full_name'],
                year_served=leader_data['year_served'],
                defaults=leader_data
            )
            if created:
                self.stdout.write(f"Created test leader: {leader.full_name}")
            else:
                self.stdout.write(f"Leader already exists: {leader.full_name}")
    
    def update_existing_leaders(self):
        """Update existing leaders to have past end dates for testing"""
        from kuai_club.models import Leader  # Replace 'myapp' with your app name
        from datetime import date
        
        # Update some leaders to be "previous" by setting end_date in the past
        leaders_to_update = Leader.objects.filter(
            end_date__isnull=True
        )[:2]  # Update first 2 leaders without end dates
        
        past_date = date(2023, 12, 31)
        
        for leader in leaders_to_update:
            leader.end_date = past_date
            leader.year_served = 2023
            leader.save()
            self.stdout.write(f"Updated leader to previous: {leader.full_name}")

