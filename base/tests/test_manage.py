# tests/test_manage.py
from django.test import TestCase
from django.core.management import execute_from_command_line
import sys

class ManageCommandTests(TestCase):
    def test_manage_command_execution(self):
        sys.argv = ['manage.py', 'help']
        try:
            execute_from_command_line(sys.argv)
            execution_successful = True
        except SystemExit:
            execution_successful = True
        except Exception:
            execution_successful = False
        
        self.assertTrue(execution_successful)