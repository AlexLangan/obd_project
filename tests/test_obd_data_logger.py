import unittest
from unittest.mock import MagicMock, patch
import obd_data_logger as obd_logger

class TestOBDDataLogger(unittest.TestCase):
    @patch("obd_data_logger.obd.OBD")  # Mock OBD class to avoid using real hardware
    def test_log_sensors(self, mock_obd_class):
        # Create a fake OBD connection
        mock_connection = MagicMock()

        # Each query returns a fake response with a dummy value
        mock_response = MagicMock()
        mock_response.is_null.return_value = False
        mock_response.value = 123  # dummy sensor value
        mock_connection.query.return_value = mock_response

        # Call log_sensors with the mocked connection
        obd_logger.log_sensors(mock_connection)

        # Check that each command was queried
        self.assertEqual(mock_connection.query.call_count, len(obd_logger.COMMANDS))

    @patch("obd_data_logger.obd.OBD")
    def test_log_dtcs_no_codes(self, mock_obd_class):
        # Mock a connection with no DTC codes
        mock_connection = MagicMock()
        mock_response = MagicMock()
        mock_response.value = []  # No trouble codes
        mock_connection.query.return_value = mock_response

        # Call log_dtcs
        obd_logger.log_dtcs(mock_connection)

        # Ensure query for DTC command was called once
        mock_connection.query.assert_called_once_with(obd_logger.obd.commands.GET_DTC)

if __name__ == "__main__":
    unittest.main()
