def modify_txt_file(file_path, changes):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("File not found:", file_path)
        return
    try:
        with open(file_path, 'w') as f:
            for line in changes:
                f.write(line)
                f.write("\n")
    except Exception as e:
        print("Error writing to file:", e)


class Components:
    match = {
        0: 'true',
        1: 'false',
        2: 'none'
    }
    instance_mode = {
        0: 'same_ontology',
        1: 'matching_classes',
        2: 'different_classes',
        3: 'auto'
    }
    word_matcher = {
        0: 'by_class',
        1: 'by_name',
        2: 'average',
        3: 'maximum',
        4: 'minimum',
        5: 'none',
        6: 'auto'
    }
    string_matcher = {
        0: 'none',
        1: 'auto',
        2: 'global',
        3: 'local'
    }
    struct_matcher = {
        0: 'none',
        1: 'auto',
        2: 'ancestors',
        3: 'descendants',
        4: 'average',
        5: 'maximum',
        6: 'minimum'
    }
    string_measure = {
        0: 'ISub',
        1: 'Levenstein',
        2: 'Jaro-Winkler',
        3: 'Q-gram'
    }
    selection_type = {
        0: 'none',
        1: 'auto',
        2: 'strict',
        3: 'permissive',
        4: 'hybrid',
    }
    def __int__(self):
        self.default_conf = {
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

    def convert_action_to_conf(self, action):
        config = {
            "match_classes": Components.match[action[0]],
            "match_properties": Components.match[action[1]],
            "match_individuals": Components.match[action[2]],
            "threshold": str((action[3] + 51) / 100),
            "match_same_uri": Components.match[action[4]],
            "instance_matching_mode": Components.instance_mode[action[5]],
            "use_translator": Components.match[action[6]],
            "bk_sources": "all",
            "word_matcher": Components.word_matcher[action[7]],
            "string_matcher": Components.string_matcher[action[8]],
            "struct_matcher": Components.struct_matcher[action[9]],
            "string_measure": Components.string_measure[action[10]],
            "selection_type": Components.selection_type[action[11]],
            "repair_alignment": Components.match[1]  # always false  -> aml loop bug
        }
        return [f"{key}={value}" for key, value in config.items()]
