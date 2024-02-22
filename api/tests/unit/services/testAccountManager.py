####################################################################################################
# Project Name: Motive Event Management System
# Course: COMP70025 - Software Systems Engineering
# File: testAccountManager.py
# Description: This file contains unit tests for each function in the accountManager.py file.
#
# Authors: James Hartley, Ankur Desai, Patrick Borman, Julius Gasson, and Vadim Dunaevskiy
# Date: 2024-02-19
# Version: 2.1
#
# Notes: Supabase interactions tested using patch and MagicMock from unittest.mock. Unit tests for
#        validate_delete_request are still outstanding.
####################################################################################################
import sys
sys.path.append('../../../services')

import unittest
from unittest.mock import patch, MagicMock
from services.accountManager import *
from services import accountManager


class TestEmailValidation(unittest.TestCase):
    def test_valid_email(self):
        self.assertTrue(is_valid_email("test@example.com"))

    def test_missing_domain(self):
        self.assertFalse(is_valid_email("test@"))

    def test_missing_at_symbol(self):
        self.assertFalse(is_valid_email("testexample.com"))

    def test_invalid_characters(self):
        self.assertFalse(is_valid_email("test@exa$mple.com"))

    def test_invalid_domain(self):
        self.assertFalse(is_valid_email("test@example"))

    def test_empty_string(self):
        self.assertFalse(is_valid_email(""))


# class TestCheckEmailInUse(unittest.TestCase):

#     @patch("accountManager.supabase")
#     def test_email_in_use(self, mock_supabase):
#         # Mock the response from Supabase
#         mock_supabase.rpc.return_value.execute.return_value.data = [
#             {"account_type": "venue", "user_id": "123"}
#         ]

#         result = check_email_in_use("test@example.com")
#         self.assertEqual(result, {"account_type": "venue", "user_id": "123"})

#     @patch("accountManager.supabase")
#     def test_email_not_in_use(self, mock_supabase):
#         # Mock the response to indicate no data found
#         mock_supabase.rpc.return_value.execute.return_value.data = []

#         result = check_email_in_use("new@example.com")
#         self.assertEqual(result, {"message": "Email is not in use."})

#     @patch("accountManager.supabase")
#     def test_invalid_email_format(self, mock_supabase):
#         # Test for invalid email format, which should not even attempt to query Supabase
#         result = check_email_in_use("invalid-email")
#         self.assertEqual(result, {"error": "Invalid email format."})

#     @patch("accountManager.supabase")
#     def test_supabase_error(self, mock_supabase):
#         # Mock an exception being raised during the Supabase call
#         mock_supabase.rpc.side_effect = Exception("Supabase query failed")

#         result = check_email_in_use("error@example.com")
#         self.assertEqual(result, {"error": "An error occurred: Supabase query failed"})


# class TestValidateRequest(unittest.TestCase):

#     def test_email_validation(self):
#         self.assertTrue(is_valid_email("test@example.com"))
#         self.assertFalse(is_valid_email("invalid-email"))

#     def test_valid_requests_with_attributes(self):
#         request = {
#             "function": "get",
#             "object_type": "venue",
#             "identifier": "venue@example.com",
#             "attributes": {"user_id": True, "location": True},
#         }
#         self.assertEqual(validate_request(request), (True, "Request is valid."))

#     def test_request_with_nonexistant_attributes(self):
#         request = {
#             "function": "get",
#             "object_type": "artist",
#             "identifier": "artist@example.com",
#             "attributes": {"user_id": True, "genre": True, "extra_field": False},
#         }
#         valid, message = validate_request(request)
#         self.assertFalse(valid)
#         self.assertIn("extra_field", message)

#     def test_invalid_email_in_request(self):
#         request = {
#             "function": "get",
#             "object_type": "artist",
#             "identifier": "invalid-email",
#             "attributes": {"user_id": True, "genre": True},
#         }
#         self.assertEqual(
#             validate_request(request), (False, "Invalid or missing email identifier.")
#         )

#     def test_missing_email(self):
#         request = {
#             "function": "get",
#             "object_type": "artist",
#             "identifier": "",
#             "attributes": {
#                 "user_id": True,
#                 "email": False,
#                 "username": False,
#                 "genre": False,
#             },
#         }
#         self.assertEqual(
#             validate_request(request), (False, "Invalid or missing email identifier.")
#         )

#     def test_event_object_type(self):
#         request = {
#             "function": "get",
#             "object_type": "event",
#             "identifier": "example@example.com",
#             "attributes": {
#                 "user_id": True,
#             },
#         }
#         self.assertEqual(
#             validate_request(request),
#             (False, "Management of events is handled by a separate API."),
#         )

#     def test_ticket_object_type(self):
#         request = {
#             "function": "get",
#             "object_type": "ticket",
#             "identifier": "example@example.com",
#             "attributes": {
#                 "user_id": True,
#             },
#         }
#         self.assertEqual(
#             validate_request(request),
#             (False, "Management of tickets is handled by a separate API."),
#         )

#     def test_invalid_account_type(self):
#         request = {
#             "function": "get",
#             "object_type": "non-defined_account_type",
#             "identifier": "example@example.com",
#             "attributes": {"user_id": True, "genre": True},
#         }
#         self.assertEqual(
#             validate_request(request),
#             (
#                 False,
#                 "Invalid object type. Must be one of "
#                 "['venue', 'artist', 'attendee'].",
#             ),
#         )

#     def test_missing_account_type(self):
#         request = {
#             "function": "get",
#             "identifier": "example@example.com",
#             "attributes": {"user_id": True, "genre": True},
#         }
#         self.assertEqual(
#             validate_request(request),
#             (
#                 False,
#                 "Invalid object type. Must be one of "
#                 "['venue', 'artist', 'attendee'].",
#             ),
#         )

#     def test_request_with_all_false_attributes(self):
#         request = {
#             "function": "get",
#             "object_type": "artist",
#             "identifier": "example@example.com",
#             "attributes": {
#                 "user_id": False,
#                 "email": False,
#                 "username": False,
#                 "genre": False,
#             },
#         }
#         self.assertEqual(
#             validate_request(request),
#             (False, "At least one valid attribute must be queried with a true value."),
#         )


# class TestExtractAndPrepareAttributes(unittest.TestCase):
#     def test_with_full_request(self):
#         request = {
#             "object_type": "artist",
#             "attributes": {"name": "John Doe", "genre": "Rock", "user_id": "12345"},
#         }
#         expected = ("artist", {"name": "John Doe", "genre": "Rock"})
#         self.assertEqual(extract_and_prepare_attributes(request), expected)

#     def test_with_user_id_present(self):
#         request = {
#             "object_type": "venue",
#             "attributes": {"location": "Downtown", "user_id": "67890"},
#         }
#         expected = ("venue", {"location": "Downtown"})
#         self.assertEqual(extract_and_prepare_attributes(request), expected)

#     def test_with_empty_attributes(self):
#         request = {"object_type": "attendee", "attributes": {}}
#         expected = ("attendee", {})
#         self.assertEqual(extract_and_prepare_attributes(request), expected)

#     def test_with_no_attributes_key(self):
#         request = {"object_type": "event"}
#         expected = ("event", {})
#         self.assertEqual(extract_and_prepare_attributes(request), expected)

#     def test_with_missing_object_type(self):
#         request = {"attributes": {"title": "Concert", "date": "2024-01-01"}}
#         expected = (None, {"title": "Concert", "date": "2024-01-01"})
#         self.assertEqual(extract_and_prepare_attributes(request), expected)

#     def test_with_additional_keys(self):
#         request = {
#             "object_type": "ticket",
#             "attributes": {"seat": "A1", "user_id": "54321"},
#             "extra_key": "extra_value",
#         }
#         expected = ("ticket", {"seat": "A1"})
#         self.assertEqual(extract_and_prepare_attributes(request), expected)


# class TestCheckForExtraAttributes(unittest.TestCase):

#     # Mock attributes_schema for testing
#     attributes_schema = {
#         "artist": {"name", "genre", "country"},
#         "venue": {"location", "capacity"},
#     }

#     @patch("accountManager.attributes_schema", attributes_schema)
#     def test_no_extra_attributes(self):
#         validation_attributes = {"name": "John Doe", "genre": "Rock"}
#         object_type = "artist"
#         self.assertTrue(
#             check_for_extra_attributes(validation_attributes, object_type)[0]
#         )

#     @patch("accountManager.attributes_schema", attributes_schema)
#     def test_with_extra_attributes(self):
#         validation_attributes = {
#             "name": "John Doe",
#             "genre": "Rock",
#             "extra": "Not Allowed",
#         }
#         object_type = "artist"
#         self.assertFalse(
#             check_for_extra_attributes(validation_attributes, object_type)[0]
#         )

#     @patch("accountManager.attributes_schema", attributes_schema)
#     def test_with_all_required_attributes(self):
#         validation_attributes = {"location": "Downtown", "capacity": 5000}
#         object_type = "venue"
#         self.assertTrue(
#             check_for_extra_attributes(validation_attributes, object_type)[0]
#         )

#     @patch("accountManager.attributes_schema", attributes_schema)
#     def test_object_type_not_in_schema(self):
#         validation_attributes = {"field": "value"}
#         object_type = "nonexistent"
#         self.assertTrue(
#             check_for_extra_attributes(validation_attributes, object_type)[0],
#             "Should return True as there are no defined attributes to violate.",
#         )

#     @patch("accountManager.attributes_schema", attributes_schema)
#     def test_empty_validation_attributes(self):
#         validation_attributes = {}
#         object_type = "artist"
#         self.assertTrue(
#             check_for_extra_attributes(validation_attributes, object_type)[0],
#             "Should return True as empty attributes cannot include extra ones.",
#         )


# class TestCheckRequiredAttributes(unittest.TestCase):
#     # Mock attributes_schema for testing
#     attributes_schema = {
#         "artist": {"name", "genre", "country"},
#         "venue": {"location", "capacity"},
#     }

#     @patch("accountManager.attributes_schema", attributes_schema)
#     def test_all_required_attributes_provided(self):
#         validation_attributes = {"name": "John Doe", "genre": "Rock", "country": "USA"}
#         object_type = "artist"
#         self.assertTrue(
#             check_required_attributes(validation_attributes, object_type)[0]
#         )

#     @patch("accountManager.attributes_schema", attributes_schema)
#     def test_missing_required_attributes(self):
#         validation_attributes = {
#             "name": "John Doe",
#             "genre": "Rock",
#         }  # Missing 'country'
#         object_type = "artist"
#         self.assertFalse(
#             check_required_attributes(validation_attributes, object_type)[0]
#         )

#     @patch("accountManager.attributes_schema", attributes_schema)
#     def test_object_type_not_in_schema(self):
#         validation_attributes = {"field": "value"}
#         object_type = "nonexistent"
#         # Assuming function should return True, as no required attributes are defined for nonexistent object types
#         self.assertTrue(
#             check_required_attributes(validation_attributes, object_type)[0],
#             "Should return True as there are no defined required attributes to miss.",
#         )

#     @patch("accountManager.attributes_schema", attributes_schema)
#     def test_empty_validation_attributes(self):
#         validation_attributes = {}
#         object_type = "artist"
#         # Since 'artist' has required attributes and none are provided, expecting False
#         self.assertFalse(
#             check_required_attributes(validation_attributes, object_type)[0],
#             "Should return False as required attributes are missing.",
#         )


# class TestGetAccountInfo(unittest.TestCase):

#     @patch("accountManager.supabase")
#     @patch("accountManager.validate_request")
#     def test_valid_request_with_account_found(self, mock_validate, mock_supabase):
#         # Mock validate_request to return valid
#         mock_validate.return_value = (True, "Request is valid.")
#         # Mock Supabase response
#         mock_supabase.table().select().eq().execute.return_value.data = [
#             {"user_id": "123"}
#         ]

#         request = {
#             "function": "get",
#             "object_type": "venue",
#             "identifier": "new@example.com",
#             "attributes": {"user_id": True, "username": True},
#         }
#         result = get_account_info(request)
#         self.assertTrue(result["in_use"])
#         self.assertIn("Email is registered with user", result["message"])

#     @patch("accountManager.supabase")
#     @patch("accountManager.validate_request")
#     def test_valid_request_no_account_found(self, mock_validate, mock_supabase):
#         mock_validate.return_value = (True, "Request is valid.")
#         mock_supabase.table().select().eq().execute.return_value.data = []

#         request = {
#             "function": "get",
#             "object_type": "venue",
#             "identifier": "new@example.com",
#             "attributes": {"user_id": True, "username": True},
#         }
#         result = get_account_info(request)
#         self.assertFalse(result["in_use"])
#         self.assertEqual(result["message"], "Email is not in use.")

#     @patch("accountManager.validate_request")
#     def test_invalid_function(self, mock_validate):
#         mock_validate.return_value = (False, "Invalid function specified.")

#         request = {
#             "function": "undefined",
#             "object_type": "unknown",
#             "identifier": "new@example.com",
#         }
#         result = get_account_info(request)
#         self.assertEqual(result, {"error": "Invalid function specified."})

#     @patch("accountManager.supabase")
#     @patch("accountManager.validate_request")
#     def test_api_error(self, mock_validate, mock_supabase):
#         mock_validate.return_value = (True, "Request is valid.")
#         mock_supabase.table().select().eq().execute.side_effect = Exception("API error")

#         request = {
#             "function": "get",
#             "object_type": "venue",
#             "identifier": "new@example.com",
#             "attributes": {"user_id": True, "username": True},
#         }
#         result = get_account_info(request)
#         self.assertTrue("error" in result)
#         self.assertEqual(result["error"], "An API error occurred: API error")


# class TestValidateGetRequest(unittest.TestCase):
#     @patch("accountManager.extract_and_prepare_attributes_for_get")
#     @patch("accountManager.validate_queried_attributes")
#     def test_successful_validation(self, mock_validate_queried, mock_extract):
#         # Setup mock responses
#         mock_extract.return_value = ("artist", {"name": True, "genre": True})
#         mock_validate_queried.return_value = (True, "")

#         request = {"object_type": "artist", "attributes": ["name", "genre"]}
#         valid, message = validate_get_request(request)

#         self.assertTrue(valid)
#         self.assertEqual(message, "Request is valid.")

#     @patch("accountManager.extract_and_prepare_attributes_for_get")
#     def test_no_attributes_provided(self, mock_extract):
#         # Setup mock response to simulate no attributes provided
#         mock_extract.return_value = ("artist", {})

#         request = {"object_type": "artist"}
#         valid, message = validate_get_request(request)

#         self.assertFalse(valid)
#         self.assertEqual(message, "Attributes must be provided for querying.")

#     @patch("accountManager.extract_and_prepare_attributes_for_get")
#     @patch("accountManager.validate_queried_attributes")
#     def test_queried_attributes_validation_fails(
#         self, mock_validate_queried, mock_extract
#     ):
#         # Setup mock responses to simulate queried attributes validation failure
#         mock_extract.return_value = ("artist", {"name": True})
#         mock_validate_queried.return_value = (False, "Invalid attribute")

#         request = {"object_type": "artist", "attributes": ["name"]}
#         valid, message = validate_get_request(request)

#         self.assertFalse(valid)
#         self.assertEqual(message, "Invalid attribute")


# class TestExtractAndPrepareAttributesForGet(unittest.TestCase):
#     def test_attributes_as_list(self):
#         request = {"object_type": "artist", "attributes": ["name", "genre"]}
#         expected = ("artist", {"name": True, "genre": True})
#         self.assertEqual(extract_and_prepare_attributes_for_get(request), expected)

#     def test_attributes_as_dict(self):
#         request = {
#             "object_type": "venue",
#             "attributes": {"location": True, "capacity": False},
#         }
#         expected = ("venue", {"location": True, "capacity": False})
#         self.assertEqual(extract_and_prepare_attributes_for_get(request), expected)

#     def test_attributes_not_provided(self):
#         request = {"object_type": "event"}
#         expected = ("event", {})
#         self.assertEqual(extract_and_prepare_attributes_for_get(request), expected)

#     def test_empty_attributes_list(self):
#         request = {"object_type": "ticket", "attributes": []}
#         expected = ("ticket", {})
#         self.assertEqual(extract_and_prepare_attributes_for_get(request), expected)

#     def test_empty_attributes_dict(self):
#         request = {"object_type": "attendee", "attributes": {}}
#         expected = ("attendee", {})
#         self.assertEqual(extract_and_prepare_attributes_for_get(request), expected)


# class TestValidateQueriedAttributes(unittest.TestCase):
#     # Setup for mock data
#     attributes_schema = {
#         "artist": ["name", "genre", "country"],
#         "venue": ["location", "capacity"],
#     }
#     account_types = ["venue", "artist", "attendee"]
#     non_account_types = ["event", "ticket"]

#     @patch("accountManager.attributes_schema", attributes_schema)
#     @patch("accountManager.account_types", account_types)
#     @patch("accountManager.non_account_types", non_account_types)
#     def test_valid_queried_attributes(self):
#         queried_attributes = {"name": True, "genre": True}
#         object_type = "artist"
#         self.assertTrue(validate_queried_attributes(queried_attributes, object_type)[0])

#     def test_invalid_attribute_in_queried_attributes(self):
#         queried_attributes = {"name": True, "invalid_attr": True}
#         object_type = "artist"
#         self.assertFalse(
#             validate_queried_attributes(queried_attributes, object_type)[0]
#         )

#     def test_non_account_type_object(self):
#         queried_attributes = {"name": True}
#         object_type = "event"
#         self.assertFalse(
#             validate_queried_attributes(queried_attributes, object_type)[0]
#         )

#     def test_invalid_object_type(self):
#         queried_attributes = {"name": True}
#         object_type = "nonexistent_type"
#         self.assertFalse(
#             validate_queried_attributes(queried_attributes, object_type)[0]
#         )

#     def test_empty_queried_attributes(self):
#         queried_attributes = {}
#         object_type = "artist"
#         self.assertFalse(
#             validate_queried_attributes(queried_attributes, object_type)[0]
#         )

#     def test_queried_attribute_with_false_value(self):
#         queried_attributes = {"name": False, "genre": True}
#         object_type = "artist"
#         self.assertFalse(
#             validate_queried_attributes(queried_attributes, object_type)[0]
#         )


# class TestCreateAccount(unittest.TestCase):
#     @patch("accountManager.validate_get_request")
#     @patch("accountManager.supabase")
#     def test_valid_request(self, mock_supabase, mock_validate):
#         mock_validate.return_value = (True, "")
#         mock_result = MagicMock()
#         mock_result.error = None
#         mock_result.data = [{"user_id": "12345"}]
#         mock_supabase.table().insert().execute.return_value = mock_result

#         user_id, message = create_account(
#             {
#                 "object_type": "artist",
#                 "identifier": "email@example.com",
#                 "attributes": {"name": True, "genre": True},
#             }
#         )

#         self.assertEqual(user_id, "12345")
#         self.assertEqual(message, "Account creation was successful.")

#     @patch("accountManager.validate_get_request")
#     def test_invalid_request(self, mock_validate):
#         mock_validate.return_value = (False, "Invalid request")

#         user_id, message = create_account(
#             {"object_type": "invalid_type", "identifier": "", "attributes": {}}
#         )

#         self.assertIsNone(user_id)
#         self.assertEqual(message, "Invalid request")

#     @patch("accountManager.validate_get_request")
#     @patch("accountManager.supabase")
#     def test_supabase_insert_error(self, mock_supabase, mock_validate):
#         mock_validate.return_value = (True, "")
#         mock_result = MagicMock()
#         mock_result.error = "Insert error"
#         mock_supabase.table().insert().execute.return_value = mock_result

#         user_id, message = create_account(
#             {
#                 "object_type": "artist",
#                 "identifier": "email@example.com",
#                 "attributes": {"name": True},
#             }
#         )

#         self.assertIsNone(user_id)
#         self.assertIn("An error occurred", message)

#     @patch("accountManager.validate_get_request")
#     @patch("accountManager.supabase")
#     def test_exception_during_insert(self, mock_supabase, mock_validate):
#         mock_validate.return_value = (True, "")
#         mock_supabase.table().insert().execute.side_effect = Exception(
#             "Database connection error"
#         )

#         user_id, message = create_account(
#             {
#                 "object_type": "artist",
#                 "identifier": "email@example.com",
#                 "attributes": {"name": True},
#             }
#         )

#         self.assertIsNone(user_id)
#         self.assertIn("An exception occurred", message)


# class TestValidateCreateRequest(unittest.TestCase):
#     @patch("accountManager.extract_and_prepare_attributes")
#     @patch("accountManager.check_required_attributes")
#     @patch("accountManager.check_for_extra_attributes")
#     def test_successful_validation(
#         self, mock_check_extra, mock_check_required, mock_extract
#     ):
#         # Setup mock responses for a successful validation path
#         mock_extract.return_value = ("artist", {"name": "John", "genre": "Rock"})
#         mock_check_required.return_value = (True, "")
#         mock_check_extra.return_value = (True, "")

#         request = {
#             "object_type": "artist",
#             "attributes": {"name": "John", "genre": "Rock"},
#         }
#         valid, message = validate_create_request(request)

#         self.assertTrue(valid)
#         self.assertEqual(message, "Request is valid.")

#     @patch("accountManager.extract_and_prepare_attributes")
#     @patch("accountManager.check_required_attributes")
#     def test_missing_required_attributes(self, mock_check_required, mock_extract):
#         # Simulate missing required attributes
#         mock_extract.return_value = ("artist", {"genre": "Rock"})
#         mock_check_required.return_value = (False, "Missing required attributes.")

#         request = {"object_type": "artist", "attributes": {"genre": "Rock"}}
#         valid, message = validate_create_request(request)

#         self.assertFalse(valid)
#         self.assertEqual(message, "Missing required attributes.")

#     @patch("accountManager.extract_and_prepare_attributes")
#     @patch("accountManager.check_for_extra_attributes")
#     def test_extra_undefined_attributes(self, mock_check_extra, mock_extract):
#         # Simulate extra undefined attributes
#         mock_extract.return_value = (
#             "artist",
#             {
#                 "email": "user@example.com",
#                 "username": "John",
#                 "genre": "",
#                 "extra_attr": "Not Allowed",
#             },
#         )
#         mock_check_extra.return_value = (
#             False,
#             "Additional, undefined attributes cannot be specified.",
#         )

#         request = {
#             "object_type": "artist",
#             "attributes": {"name": "John", "extra_attr": "Not Allowed"},
#         }
#         valid, message = validate_create_request(request)

#         self.assertFalse(valid)
#         self.assertEqual(
#             message, "Additional, undefined attributes cannot be specified."
#         )

#     @patch("accountManager.extract_and_prepare_attributes")
#     def test_attributes_without_value(self, mock_extract):
#         # Simulate an attribute without a value
#         mock_extract.return_value = (
#             "artist",
#             {"email": "user@example.com", "username": "John", "genre": ""},
#         )

#         request = {
#             "object_type": "artist",
#             "attributes": {
#                 "email": "user@example.com",
#                 "username": "John",
#                 "genre": "",
#             },
#         }
#         valid, message = validate_create_request(request)

#         self.assertFalse(valid)
#         self.assertEqual(message, "Every specified attribute must have a value.")


# class TestUpdateAccount(unittest.TestCase):
#     @patch("accountManager.validate_request")
#     @patch("accountManager.supabase")
#     def test_valid_update_request(self, mock_supabase, mock_validate):
#         # Setup mock responses
#         mock_validate.return_value = (True, "")
#         mock_result = MagicMock()
#         mock_result.error = None
#         mock_supabase.table().update().eq().execute.return_value = mock_result

#         request = {
#             "object_type": "artist",
#             "identifier": "artist_id_123",
#             "attributes": {"email": "new_email@example.com"},
#         }
#         success, message = update_account(request)

#         self.assertTrue(success)
#         self.assertEqual(message, "Account update was successful.")

#     @patch("accountManager.validate_request")
#     def test_invalid_request_structure(self, mock_validate):
#         mock_validate.return_value = (False, "Invalid request structure")

#         request = {}  # Simulating an invalid request
#         success, message = update_account(request)

#         self.assertFalse(success)
#         self.assertEqual(message, "Invalid request structure")

#     @patch("accountManager.validate_request")
#     def test_no_valid_attributes_for_update(self, mock_validate):
#         mock_validate.return_value = (True, "")

#         request = {
#             "object_type": "artist",
#             "identifier": "artist_id_123",
#             "attributes": {"email": None},  # No valid attributes to update
#         }
#         success, message = update_account(request)

#         self.assertFalse(success)
#         self.assertEqual(message, "No valid attributes provided for update.")

#     @patch("accountManager.validate_request")
#     @patch("accountManager.supabase")
#     def test_supabase_update_error(self, mock_supabase, mock_validate):
#         mock_validate.return_value = (True, "")
#         mock_result = MagicMock()
#         mock_result.error = "Supabase error"
#         mock_supabase.table().update().eq().execute.return_value = mock_result

#         request = {
#             "object_type": "artist",
#             "identifier": "artist_id_123",
#             "attributes": {"username": "new_username"},
#         }
#         success, message = update_account(request)

#         self.assertFalse(success)
#         self.assertIn("An error occurred: Supabase error", message)

#     @patch("accountManager.validate_request")
#     @patch("accountManager.supabase")
#     def test_exception_during_update_operation(self, mock_supabase, mock_validate):
#         mock_validate.return_value = (True, "")
#         mock_supabase.table().update().eq().execute.side_effect = Exception(
#             "Database error"
#         )

#         request = {
#             "object_type": "artist",
#             "identifier": "artist_id_123",
#             "attributes": {"genre": "new_genre"},
#         }
#         success, message = update_account(request)

#         self.assertFalse(success)
#         self.assertIn("An exception occurred: Database error", message)


# class TestValidateUpdateRequest(unittest.TestCase):
#     @patch("accountManager.extract_and_prepare_attributes")
#     @patch("accountManager.check_for_extra_attributes")
#     def test_valid_update_request(self, mock_check_extra, mock_extract):
#         # Setup mock responses for a successful validation
#         mock_extract.return_value = ("artist", {"name": "New Artist Name"})
#         mock_check_extra.return_value = (True, "")

#         request = {"object_type": "artist", "attributes": {"name": "New Artist Name"}}
#         valid, message = validate_update_request(request)

#         self.assertTrue(valid)
#         self.assertEqual(message, "Request is valid.")

#     @patch("accountManager.extract_and_prepare_attributes")
#     def test_no_attributes_specified_for_update(self, mock_extract):
#         # Simulate no attributes provided for update
#         mock_extract.return_value = ("artist", {})

#         request = {"object_type": "artist", "attributes": {}}
#         valid, message = validate_update_request(request)

#         self.assertFalse(valid)
#         self.assertEqual(
#             message, "At least one attribute must be specified for update."
#         )

#     @patch("accountManager.extract_and_prepare_attributes")
#     @patch("accountManager.check_for_extra_attributes")
#     def test_extra_undefined_attributes_provided(self, mock_check_extra, mock_extract):
#         # Simulate extra, undefined attributes provided
#         mock_extract.return_value = ("artist", {"undefined_attr": "value"})
#         mock_check_extra.return_value = (
#             False,
#             "Additional, undefined attributes cannot be specified.",
#         )

#         request = {"object_type": "artist", "attributes": {"undefined_attr": "value"}}
#         valid, message = validate_update_request(request)

#         self.assertFalse(valid)
#         self.assertEqual(
#             message, "Additional, undefined attributes cannot be specified."
#         )

#     @patch("accountManager.extract_and_prepare_attributes")
#     @patch("accountManager.check_for_extra_attributes")
#     def test_valid_request_with_multiple_attributes(
#         self, mock_check_extra, mock_extract
#     ):
#         # Setup for a valid request with multiple attributes
#         mock_extract.return_value = (
#             "venue",
#             {"location": "New Location", "capacity": 5000},
#         )
#         mock_check_extra.return_value = (True, "")

#         request = {
#             "object_type": "venue",
#             "attributes": {"location": "New Location", "capacity": 5000},
#         }
#         valid, message = validate_update_request(request)

#         self.assertTrue(valid)
#         self.assertEqual(message, "Request is valid.")


# class TestDeleteAccount(unittest.TestCase):
#     @patch("accountManager.validate_request")
#     @patch("accountManager.supabase")
#     def test_valid_delete_request(self, mock_supabase, mock_validate):
#         # Setup mock responses
#         mock_validate.return_value = (True, "")
#         mock_result = MagicMock()
#         mock_result.error = None
#         mock_supabase.table().delete().eq().execute.return_value = mock_result

#         request = {
#             "object_type": "artist",
#             "identifier": "artist_id_123",
#         }
#         success, message = delete_account(request)

#         self.assertTrue(success)
#         self.assertEqual(message, "Account deletion was successful.")

#     @patch("accountManager.validate_request")
#     def test_invalid_request_structure(self, mock_validate):
#         mock_validate.return_value = (False, "Invalid request structure")

#         request = {}  # Simulating an invalid request
#         success, message = delete_account(request)

#         self.assertFalse(success)
#         self.assertEqual(message, "Invalid request structure")

#     @patch("accountManager.validate_request")
#     @patch("accountManager.supabase")
#     def test_supabase_delete_error(self, mock_supabase, mock_validate):
#         mock_validate.return_value = (True, "")
#         mock_result = MagicMock()
#         mock_result.error = "Supabase error"
#         mock_supabase.table().delete().eq().execute.return_value = mock_result

#         request = {
#             "object_type": "artist",
#             "identifier": "artist_id_123",
#         }
#         success, message = delete_account(request)

#         self.assertFalse(success)
#         self.assertIn("An error occurred: Supabase error", message)

#     @patch("accountManager.validate_request")
#     @patch("accountManager.supabase")
#     def test_exception_during_delete_operation(self, mock_supabase, mock_validate):
#         mock_validate.return_value = (True, "")
#         mock_supabase.table().delete().eq().execute.side_effect = Exception(
#             "Database error"
#         )

#         request = {
#             "object_type": "artist",
#             "identifier": "artist_id_123",
#         }
#         success, message = delete_account(request)

#         self.assertFalse(success)
#         self.assertIn("An exception occurred: Database error", message)


# # class TestValidateDeleteRequest(unittest.TestCase):
# # TBC when additional logic provided to make deletion more secure

if __name__ == "__main__":
    unittest.main()
