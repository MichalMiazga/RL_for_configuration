import unittest

from connector import RewardProcessor, run_command_and_read_last_line


class ConnectorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create an instance of the connector
        cls.connector = RewardProcessor()
        config = {
            "match_classes": "auto",
            "match_properties": "auto",
            "match_individuals": "auto",
            "threshold": "0.9",
            "match_same_uri": "false",
            "instance_matching_mode": "auto",
            "use_translator": "auto",
            "bk_sources": "all",
            "word_matcher": "none",
            "string_matcher": "none",
            "struct_matcher": "auto",
            "string_measure": "ISub",
            "selection_type": "auto",
            "repair_alignment": "true"
        }
        cls.config_list = [f"{key}={value}" for key, value in config.items()]
        config2 = {
            "match_classes": "auto",
            "match_properties": "auto",
            "match_individuals": "auto",
            "threshold": "0.6",
            "match_same_uri": "false",
            "instance_matching_mode": "auto",
            "use_translator": "auto",
            "bk_sources": "all",
            "word_matcher": "none",
            "string_matcher": "none",
            "struct_matcher": "auto",
            "string_measure": "ISub",
            "selection_type": "auto",
            "repair_alignment": "true"
        }
        cls.config_list2 = [f"{key}={value}" for key, value in config2.items()]

    def test_init(self):
        print(self.connector.execute(self.config_list))
        print(self.connector.execute(self.config_list2))
        print("Terminal run :" + str(run_command_and_read_last_line(self.config_list)))
        print("Terminal run :" + str(run_command_and_read_last_line(self.config_list2)))
