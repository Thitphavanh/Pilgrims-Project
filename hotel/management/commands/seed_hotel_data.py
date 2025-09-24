# hotel/management/commands/seed_hotel_data.py

from django.core.management.base import BaseCommand
from hotel.models import (
    RoomType, Room, Amenity, RoomAmenity, Hotel, Booking, Review
)
from datetime import date, timedelta
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Seeds the database with hotel mockup data including room types, rooms, amenities, and bookings.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing hotel data before adding new ones',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Deleting existing hotel data...'))
            Booking.objects.all().delete()
            RoomAmenity.objects.all().delete()
            Room.objects.all().delete()
            RoomType.objects.all().delete()
            Amenity.objects.all().delete()
            Hotel.objects.all().delete()
            Review.objects.all().delete()

        self.stdout.write('Creating hotel data...')

        # Create amenities first
        amenities_data = [
            {'name': 'Wi-Fi', 'description': 'Free wireless internet access', 'icon': 'fas fa-wifi', 'icon_color': 'blue', 'is_premium': False},
            {'name': 'Air Conditioning', 'description': 'Climate controlled room', 'icon': 'fas fa-snowflake', 'icon_color': 'teal', 'is_premium': False},
            {'name': 'TV', 'description': 'Flat screen television with cable', 'icon': 'fas fa-tv', 'icon_color': 'gray', 'is_premium': False},
            {'name': 'Mini Fridge', 'description': 'In-room refrigerator', 'icon': 'fas fa-cube', 'icon_color': 'blue', 'is_premium': False},
            {'name': 'Balcony', 'description': 'Private balcony with view', 'icon': 'fas fa-home', 'icon_color': 'green', 'is_premium': True},
            {'name': 'Kitchenette', 'description': 'Small kitchen with basic appliances', 'icon': 'fas fa-utensils', 'icon_color': 'orange', 'is_premium': True},
            {'name': 'Safe', 'description': 'In-room security safe', 'icon': 'fas fa-lock', 'icon_color': 'red', 'is_premium': False},
            {'name': 'Hair Dryer', 'description': 'Bathroom hair dryer', 'icon': 'fas fa-wind', 'icon_color': 'purple', 'is_premium': False},
            {'name': 'Coffee Maker', 'description': 'In-room coffee/tea maker', 'icon': 'fas fa-coffee', 'icon_color': 'yellow', 'is_premium': False},
            {'name': 'Jacuzzi', 'description': 'Private jacuzzi in room', 'icon': 'fas fa-bath', 'icon_color': 'indigo', 'is_premium': True},
            {'name': 'Work Desk', 'description': 'Dedicated workspace', 'icon': 'fas fa-laptop', 'icon_color': 'gray', 'is_premium': False},
            {'name': 'Room Service', 'description': '24/7 room service available', 'icon': 'fas fa-concierge-bell', 'icon_color': 'pink', 'is_premium': True},
        ]

        amenities = {}
        for amenity_data in amenities_data:
            amenity, created = Amenity.objects.get_or_create(
                name=amenity_data['name'],
                defaults=amenity_data
            )
            amenities[amenity_data['name']] = amenity
            if created:
                self.stdout.write(f'  - Created amenity: {amenity.name}')

        # Create room types
        room_types_data = [
            {
                'name': 'Standard Room',
                'description': 'Comfortable room with essential amenities for a pleasant stay',
                'price_per_night': Decimal('75000'),
                'capacity': 2,
                'size_sqm': 25,
                'bed_type': 'Queen Bed',
                'has_wifi': True,
                'has_ac': True,
                'has_tv': True,
                'has_balcony': False,
                'has_kitchenette': False,
                'is_featured': False,
                'amenities': ['Wi-Fi', 'Air Conditioning', 'TV', 'Safe', 'Hair Dryer']
            },
            {
                'name': 'Deluxe Room',
                'description': 'Spacious room with enhanced amenities and city view',
                'price_per_night': Decimal('95000'),
                'capacity': 2,
                'size_sqm': 35,
                'bed_type': 'King Bed',
                'has_wifi': True,
                'has_ac': True,
                'has_tv': True,
                'has_balcony': True,
                'has_kitchenette': False,
                'is_featured': True,
                'amenities': ['Wi-Fi', 'Air Conditioning', 'TV', 'Mini Fridge', 'Balcony', 'Safe', 'Hair Dryer', 'Coffee Maker', 'Work Desk']
            },
            {
                'name': 'Family Suite',
                'description': 'Large suite perfect for families with separate living area',
                'price_per_night': Decimal('135000'),
                'capacity': 4,
                'size_sqm': 50,
                'bed_type': '2 Queen Beds',
                'has_wifi': True,
                'has_ac': True,
                'has_tv': True,
                'has_balcony': True,
                'has_kitchenette': True,
                'is_featured': True,
                'amenities': ['Wi-Fi', 'Air Conditioning', 'TV', 'Mini Fridge', 'Balcony', 'Kitchenette', 'Safe', 'Hair Dryer', 'Coffee Maker', 'Work Desk']
            },
            {
                'name': 'Business Suite',
                'description': 'Executive suite with office space and premium amenities',
                'price_per_night': Decimal('155000'),
                'capacity': 2,
                'size_sqm': 45,
                'bed_type': 'King Bed',
                'has_wifi': True,
                'has_ac': True,
                'has_tv': True,
                'has_balcony': True,
                'has_kitchenette': False,
                'is_featured': False,
                'amenities': ['Wi-Fi', 'Air Conditioning', 'TV', 'Mini Fridge', 'Balcony', 'Safe', 'Hair Dryer', 'Coffee Maker', 'Work Desk', 'Room Service']
            },
            {
                'name': 'Luxury Suite',
                'description': 'Premium suite with jacuzzi and all luxury amenities',
                'price_per_night': Decimal('225000'),
                'capacity': 2,
                'size_sqm': 65,
                'bed_type': 'King Bed',
                'has_wifi': True,
                'has_ac': True,
                'has_tv': True,
                'has_balcony': True,
                'has_kitchenette': True,
                'is_featured': True,
                'amenities': ['Wi-Fi', 'Air Conditioning', 'TV', 'Mini Fridge', 'Balcony', 'Kitchenette', 'Jacuzzi', 'Safe', 'Hair Dryer', 'Coffee Maker', 'Work Desk', 'Room Service']
            }
        ]

        room_types = {}
        for rt_data in room_types_data:
            amenity_list = rt_data.pop('amenities', [])
            room_type, created = RoomType.objects.get_or_create(
                name=rt_data['name'],
                defaults=rt_data
            )
            room_types[rt_data['name']] = room_type
            if created:
                self.stdout.write(f'  - Created room type: {room_type.name} - {room_type.price_per_night} LAK')

        # Create hotel
        hotel_data = {
            'name': 'Pilgrims Venture Hotel',
            'description': 'A modern hotel offering comfortable accommodation with excellent service in the heart of the city.',
            'address': '123 Main Street, Vientiane, Laos',
            'phone': '+856 21 123 456',
            'email': 'info@pilgrimsventure.com',
            'website': 'https://pilgrimsventure.com',
            'has_restaurant': True,
            'has_gym': True,
            'has_pool': True,
            'has_spa': True,
            'has_parking': True,
            'is_active': True
        }

        hotel, created = Hotel.objects.get_or_create(
            name=hotel_data['name'],
            defaults=hotel_data
        )
        if created:
            self.stdout.write(f'  - Created hotel: {hotel.name}')

        # Create rooms
        rooms_data = []
        room_number = 101
        view_types = ['city', 'garden', 'pool', 'courtyard']

        for room_type_name, room_type in room_types.items():
            # Create 2-3 rooms per type
            room_count = 3 if room_type_name in ['Standard Room', 'Deluxe Room'] else 2

            for i in range(room_count):
                floor = (room_number // 100)
                view_type = random.choice(view_types)

                room_data = {
                    'room_type': room_type,
                    'is_checked_in': random.choice([False, False, False, True]),  # 25% checked in
                    'is_out_of_order': False,
                    'last_cleaned': date.today() - timedelta(days=random.randint(0, 2))
                }

                room, created = Room.objects.get_or_create(
                    room_type=room_type,
                    defaults=room_data
                )

                if created:
                    # Add amenities to room
                    room_amenities = room_types_data[list(room_types.keys()).index(room_type_name)].get('amenities', [])
                    for amenity_name in room_amenities:
                        if amenity_name in amenities:
                            RoomAmenity.objects.create(
                                room=room,
                                amenity=amenities[amenity_name],
                                is_available=True,
                                additional_info=f"Available in Room {room.id}"
                            )

                    self.stdout.write(f'  - Created room: Room {room.id} ({room_type_name})')

                room_number += 1

        # Create some bookings
        self.stdout.write('Creating sample bookings...')
        guest_names = [
            'John Smith', 'Sarah Johnson', 'Michael Brown', 'Emma Wilson',
            'David Lee', 'Lisa Chen', 'Robert Taylor', 'Maria Garcia',
            'James Anderson', 'Jennifer Martinez', 'William Rodriguez',
            'Elizabeth Hernandez', 'Charles Thompson', 'Susan White'
        ]

        rooms = Room.objects.all()
        booking_count = 0

        for i in range(15):  # Create 15 bookings
            room = random.choice(rooms)
            guest_name = random.choice(guest_names)
            guest_email = f"{guest_name.lower().replace(' ', '.')}@email.com"

            # Random dates in the past and future
            days_offset = random.randint(-30, 60)
            check_in = date.today() + timedelta(days=days_offset)
            nights = random.randint(1, 7)
            check_out = check_in + timedelta(days=nights)

            guests_count = random.randint(1, room.room_type.capacity)
            total_amount = room.room_type.price_per_night * nights

            # Add service fees and taxes
            service_fee = total_amount * Decimal('0.1')
            taxes = total_amount * Decimal('0.12')
            total_amount += service_fee + taxes

            status_choices = ['confirmed', 'checked_in', 'checked_out', 'pending']
            if check_in < date.today():
                status = random.choice(['checked_out', 'checked_in'])
            elif check_in == date.today():
                status = random.choice(['confirmed', 'checked_in'])
            else:
                status = random.choice(['confirmed', 'pending'])

            special_requests = [
                '', '', '',  # Most bookings have no special requests
                'Late check-in requested',
                'Extra pillows needed',
                'Non-smoking room preferred',
                'High floor room requested',
                'Quiet room away from elevator',
                'Early check-in if possible'
            ]

            booking_data = {
                'room': room,
                'guest_name': guest_name,
                'guest_email': guest_email,
                'guest_phone': f"+856 {random.randint(20000000, 99999999)}",
                'check_in_date': check_in,
                'check_out_date': check_out,
                'guests_count': guests_count,
                'total_amount': total_amount,
                'special_requests': random.choice(special_requests),
                'status': status
            }

            booking, created = Booking.objects.get_or_create(
                room=room,
                guest_email=guest_email,
                check_in_date=check_in,
                defaults=booking_data
            )

            if created:
                booking_count += 1
                self.stdout.write(f'  - Created booking: {guest_name} - Room {room.room_number} ({check_in} to {check_out})')

        # Create some reviews
        self.stdout.write('Creating sample reviews...')
        reviewer_names = [
            'Alex Thompson', 'Sophie Chen', 'Mark Johnson', 'Rachel Davis',
            'Tom Wilson', 'Anna Rodriguez', 'Kevin Lee', 'Maya Patel',
            'Chris Brown', 'Olivia Taylor', 'Daniel Kim', 'Grace Wang'
        ]

        review_texts = [
            "Excellent service and clean rooms. The staff was very helpful and accommodating.",
            "Great location and comfortable stay. Would definitely recommend this hotel.",
            "The room was spacious and well-maintained. Breakfast was delicious.",
            "Friendly staff and good amenities. The pool area was especially nice.",
            "Clean, comfortable, and good value for money. Will stay here again.",
            "Outstanding hospitality and attention to detail. Exceeded expectations.",
            "Perfect location for exploring the city. Rooms were quiet and comfortable.",
            "Professional service and modern facilities. Very satisfied with our stay.",
            "The hotel exceeded our expectations in every way. Highly recommended.",
            "Great experience overall. The staff went above and beyond to help us.",
            "Beautiful property with excellent amenities. The restaurant was fantastic.",
            "Comfortable rooms and excellent service. The location is perfect for tourists."
        ]

        for i in range(10):
            reviewer_name = random.choice(reviewer_names)
            review_text = random.choice(review_texts)
            rating = random.randint(4, 5)  # Most reviews are positive

            review_data = {
                'name': reviewer_name,
                'email': f"{reviewer_name.lower().replace(' ', '.')}@email.com",
                'rating': rating,
                'comment': review_text,
                'is_approved': True
            }

            review, created = Review.objects.get_or_create(
                name=reviewer_name,
                email=review_data['email'],
                defaults=review_data
            )

            if created:
                self.stdout.write(f'  - Created review: {reviewer_name} - {rating}/5 stars')

        # Summary
        total_rooms = Room.objects.count()
        total_room_types = RoomType.objects.count()
        total_amenities = Amenity.objects.count()
        total_bookings = Booking.objects.count()
        total_reviews = Review.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created hotel data:\n'
                f'  - 1 Hotel property\n'
                f'  - {total_room_types} Room types\n'
                f'  - {total_rooms} Rooms\n'
                f'  - {total_amenities} Amenities\n'
                f'  - {total_bookings} Bookings\n'
                f'  - {total_reviews} Reviews'
            )
        )