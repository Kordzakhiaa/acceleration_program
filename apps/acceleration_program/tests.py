from datetime import date

from django.test import TestCase
from django.utils import timezone

from apps.acceleration_program.models import AccelerationProgram
from apps.directions.models import Direction


class AccelerationProgramTestCase(TestCase):
    def setUp(self):
        self.direction = Direction.objects.create(title='Test Direction', number_of_stages=3)
        self.program = AccelerationProgram.objects.create(
            name='Test Program',
            requirements='Test Requirements',
            program_start_date=date(2023, 1, 1),
            program_end_date=date(2023, 12, 31),
            registration_start_date=date(2022, 1, 1),
            registration_end_date=date(2022, 12, 31),
            is_active=True
        )
        self.program.directions.add(self.direction)

    def test_model_creation(self):
        program = AccelerationProgram.objects.get(name='Test Program')
        self.assertEqual(program.name, 'Test Program')
        self.assertEqual(program.requirements, 'Test Requirements')
        self.assertEqual(program.program_start_date, date(2023, 1, 1))
        self.assertEqual(program.program_end_date, date(2023, 12, 31))
        self.assertEqual(program.registration_start_date, date(2022, 1, 1))
        self.assertEqual(program.registration_end_date, date(2022, 12, 31))
        self.assertEqual(program.is_active, True)
        self.assertEqual(program.directions.count(), 1)
        self.assertEqual(program.directions.first(), self.direction)

    def test_model_str_representation(self):
        program = AccelerationProgram.objects.get(name='Test Program')
        expected_str = "Test Program - active=True"
        self.assertEqual(str(program), expected_str)

    def test_model_default_values(self):
        program = AccelerationProgram.objects.create(
            name='Test Program',
            requirements='Test Requirements',
            program_start_date=date(2023, 1, 1),
            program_end_date=date(2023, 12, 31),
            registration_start_date=date(2022, 1, 1),
            registration_end_date=date(2022, 12, 31),
            is_active=True
        )
        self.assertEqual(program.is_active, True)
        self.assertEqual(program.created_at.date(), timezone.now().date())
        program.delete()

    def test_model_update(self):
        program = AccelerationProgram.objects.get(name='Test Program')
        program.name = 'Updated Program'
        program.is_active = False
        program.save()
        updated_program = AccelerationProgram.objects.get(pk=program.pk)
        self.assertEqual(updated_program.name, 'Updated Program')
        self.assertEqual(updated_program.is_active, False)

    def test_model_deletion(self):
        program = AccelerationProgram.objects.get(name='Test Program')
        program.delete()
        self.assertFalse(AccelerationProgram.objects.filter(name='Test Program').exists())

    def tearDown(self) -> None:
        self.direction.delete()
        self.program.delete()
