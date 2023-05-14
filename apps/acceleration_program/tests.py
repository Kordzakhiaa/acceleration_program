from datetime import date
from io import StringIO
from unittest import mock

from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken

from apps.acceleration_program.models import (
    AccelerationProgram,
    AssignmentType,
    Assignment,
    Stage,
    JoinProgram,
    Applicants,
)
from apps.accounts.models import CustomUserModel
from apps.directions.models import Direction


class ApplicantModelViewSetTestCase(APITestCase):
    def setUp(self):
        self.direction = Direction.objects.create(title="Test Direction", number_of_stages=3)  # noqa
        self.program = AccelerationProgram.objects.create(
            name="Test Program",
            requirements="Test Requirements",
            program_start_date=date(2023, 1, 1),
            program_end_date=date(2023, 12, 31),
            registration_start_date=date(2022, 1, 1),
            registration_end_date=date(2022, 12, 31),
            is_active=True,
        )
        self.join_program = JoinProgram.objects.create(program=self.program, direction=self.direction)
        self.client = APIClient()
        User = get_user_model()  # noqa
        self.user = User.objects.create_user(email="testuser@example.com", password="testpass")
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_list_applicants(self):
        Applicants.objects.create(program_to_join=self.join_program, applicant=self.user)

        url = reverse("acceleration_program:applicant-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["program_to_join"], self.join_program.pk)

    def test_retrieve_applicant(self):
        applicant = Applicants.objects.create(program_to_join=self.join_program, applicant=self.user)

        url = reverse("acceleration_program:applicant-detail", args=[applicant.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["program_to_join"], self.join_program.pk)

    def test_create_applicant(self):
        url = reverse("acceleration_program:applicant-list")
        data = {
            "program_to_join": self.join_program.pk,
            "applicant": self.user.pk,
            "request_status": Applicants.RequestStatuses.PENDING,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["program_to_join"], self.join_program.pk)
        self.assertEqual(Applicants.objects.count(), 1)

    def test_update_applicant(self):
        applicant = Applicants.objects.create(program_to_join=self.join_program, applicant=self.user)
        url = reverse("acceleration_program:applicant-detail", args=[applicant.pk])
        data = {
            "program_to_join": self.join_program.pk,
            "applicant": self.user.pk,
            "request_status": Applicants.RequestStatuses.ACCEPTED,
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["request_status"], Applicants.RequestStatuses.ACCEPTED)

    def test_delete_applicant(self):
        applicant = Applicants.objects.create(program_to_join=self.join_program, applicant=self.user)
        url = reverse("acceleration_program:applicant-detail", args=[applicant.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Applicants.objects.count(), 0)


class AccelerationProgramTestCase(TestCase):
    def setUp(self):
        self.direction = Direction.objects.create(title="Test Direction", number_of_stages=3)
        self.program = AccelerationProgram.objects.create(
            name="Test Program",
            requirements="Test Requirements",
            program_start_date=date(2023, 1, 1),
            program_end_date=date(2023, 12, 31),
            registration_start_date=date(2022, 1, 1),
            registration_end_date=date(2022, 12, 31),
            is_active=True,
        )
        self.program.directions.add(self.direction)

    def test_model_creation(self):
        program = AccelerationProgram.objects.get(name="Test Program")
        self.assertEqual(program.name, "Test Program")
        self.assertEqual(program.requirements, "Test Requirements")
        self.assertEqual(program.program_start_date, date(2023, 1, 1))
        self.assertEqual(program.program_end_date, date(2023, 12, 31))
        self.assertEqual(program.registration_start_date, date(2022, 1, 1))
        self.assertEqual(program.registration_end_date, date(2022, 12, 31))
        self.assertEqual(program.is_active, True)
        self.assertEqual(program.directions.count(), 1)
        self.assertEqual(program.directions.first(), self.direction)

    def test_model_str_representation(self):
        program = AccelerationProgram.objects.get(name="Test Program")
        expected_str = "Test Program - active=True"
        self.assertEqual(str(program), expected_str)

    def test_model_default_values(self):
        program = AccelerationProgram.objects.create(
            name="Test Program",
            requirements="Test Requirements",
            program_start_date=date(2023, 1, 1),
            program_end_date=date(2023, 12, 31),
            registration_start_date=date(2022, 1, 1),
            registration_end_date=date(2022, 12, 31),
            is_active=True,
        )
        self.assertEqual(program.is_active, True)
        self.assertEqual(program.created_at.date(), timezone.now().date())
        program.delete()

    def test_model_update(self):
        program = AccelerationProgram.objects.get(name="Test Program")
        program.name = "Updated Program"
        program.is_active = False
        program.save()
        updated_program = AccelerationProgram.objects.get(pk=program.pk)
        self.assertEqual(updated_program.name, "Updated Program")
        self.assertEqual(updated_program.is_active, False)

    def test_model_deletion(self):
        program = AccelerationProgram.objects.get(name="Test Program")
        program.delete()
        self.assertFalse(AccelerationProgram.objects.filter(name="Test Program").exists())

    def tearDown(self) -> None:
        self.direction.delete()
        self.program.delete()


class AssignmentTypeTestCase(TestCase):
    def setUp(self):
        self.assignment_type = AssignmentType.objects.create(type="Test Type")

    def test_model_creation(self):
        # Test if the model was created successfully.
        assignment_type = AssignmentType.objects.get(type="Test Type")
        self.assertEqual(assignment_type.type, "Test Type")

    def test_model_str_representation(self):
        # Test the string representation of the model.
        assignment_type = AssignmentType.objects.get(type="Test Type")
        self.assertEqual(str(assignment_type), "Test Type")


class AssignmentTestCase(TestCase):
    def setUp(self):
        self.assignment_type = AssignmentType.objects.create(type="Test Type")
        self.assignment = Assignment.objects.create(type=self.assignment_type, description="Test Description")

    def test_model_creation(self):
        assignment = Assignment.objects.get(description="Test Description")
        self.assertEqual(assignment.type, self.assignment_type)
        self.assertEqual(assignment.description, "Test Description")

    def test_model_str_representation(self):
        assignment = Assignment.objects.get(description="Test Description")
        expected_str = f"Assignment_Type={self.assignment_type}"
        self.assertEqual(str(assignment), expected_str)

    def test_model_type_foreign_key(self):
        assignment = Assignment.objects.get(description="Test Description")
        self.assertEqual(assignment.type, self.assignment_type)

    def test_model_type_on_delete_protect(self):
        with self.assertRaises(ProtectedError):
            self.assignment_type.delete()
        self.assertTrue(Assignment.objects.filter(type=self.assignment_type).exists())


class StageTestCase(TestCase):
    def setUp(self):
        self.assignment_type = AssignmentType.objects.create(type="Test Type")
        self.assignment = Assignment.objects.create(type=self.assignment_type, description="Test Assignment")
        self.stage = Stage.objects.create(assignment=self.assignment, name="Test Stage")

    def test_model_creation(self):
        stage = Stage.objects.get(name="Test Stage", assignment=self.assignment)
        self.assertEqual(stage.assignment, self.assignment)
        self.assertEqual(stage.name, "Test Stage")

    def test_model_str_representation(self):
        stage = Stage.objects.get(name="Test Stage")
        self.assertEqual(str(stage), "name=Test Stage")

    def test_model_assignment_foreign_key(self):
        stage = Stage.objects.get(name="Test Stage")
        self.assertEqual(stage.assignment, self.assignment)

    def test_model_assignment_on_delete_protect(self):
        with mock.patch("sys.stdout", new=StringIO()):
            with self.assertRaises(ProtectedError) as cm:
                self.assignment.delete()

        expected_error_message = (
            "Cannot delete some instances of model 'Assignment' "
            "because they are referenced through protected foreign keys: 'Stage.assignment'."
        )
        self.assertTrue(expected_error_message in str(cm.exception))
        self.assertTrue(Assignment.objects.filter(pk=self.assignment.pk).exists())

    def test_model_assignment_cascade_deletion(self):
        self.stage.delete()
        self.assignment.delete()
        self.assertFalse(Stage.objects.filter(name="Test Stage").exists())


class JoinProgramTestCase(TestCase):
    def setUp(self):
        self.assignment_type = AssignmentType.objects.create(type="Test Type")
        self.assignment = Assignment.objects.create(type=self.assignment_type, description="Test Description")
        self.direction = Direction.objects.create(title="Test Direction", number_of_stages=3)  # noqa
        self.program = AccelerationProgram.objects.create(
            name="Test Program",
            requirements="Test Requirements",
            program_start_date=date(2023, 1, 1),
            program_end_date=date(2023, 12, 31),
            registration_start_date=date(2022, 1, 1),
            registration_end_date=date(2022, 12, 31),
            is_active=True,
        )
        self.stage = Stage.objects.create(assignment=self.assignment, name="Test Stage")
        self.user = CustomUserModel.objects.create(email="testuser@example.com")

    def test_model_creation(self):
        join_program = JoinProgram.objects.create(program=self.program, direction=self.direction)
        join_program.applicants.add(self.user)  # noqa
        join_program.stages_data.add(self.stage)

        self.assertEqual(join_program.program, self.program)
        self.assertEqual(join_program.direction, self.direction)
        self.assertEqual(join_program.joined_applicants, 0)

    def test_unique_together_constraint(self):
        JoinProgram.objects.create(program=self.program, direction=self.direction)
        with self.assertRaises(Exception):
            JoinProgram.objects.create(program=self.program, direction=self.direction)

    def test_applicants_relationship(self):
        join_program = JoinProgram.objects.create(program=self.program, direction=self.direction)  # noqa
        join_program.applicants.add(self.user)  # noqa

        applicants = join_program.applicants.all()
        self.assertEqual(len(applicants), 1)
        self.assertEqual(applicants[0], self.user)

    def test_stages_data_relationship(self):
        join_program = JoinProgram.objects.create(program=self.program, direction=self.direction)  # noqa
        join_program.stages_data.add(self.stage)

        stages = join_program.stages_data.all()
        self.assertEqual(len(stages), 1)
        self.assertEqual(stages[0], self.stage)

    def test_joined_applicants_default_value(self):
        join_program = JoinProgram.objects.create(program=self.program, direction=self.direction)
        self.assertEqual(join_program.joined_applicants, 0)
