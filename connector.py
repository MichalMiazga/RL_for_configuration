import subprocess

import jpype
from jpype import JPackage, JClass
import jpype.imports

from config_edit import modify_txt_file


def run_command_and_read_last_line(config_list):
    modify_txt_file('AML/store/config.ini', config_list)
    try:
        command = ["java", "-jar", "AML/AgreementMakerLight.jar", "-m", "-s", "AML/store/anatomy/human.owl",
                   "-t",
                   "AML/store/anatomy/mouse.owl", "-i", "AML/store/anatomy/reference.rdf"]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print("Error running command:")
            print(stderr)
            return None

        # Split the output into lines and return the last line
        output_lines = stdout.strip().split('\n')
        if output_lines:
            third_value_str = output_lines[-1].split('\t')[2]
            third_value_str = third_value_str.replace('%', '')  # Remove the percentage sign
            third_value_float = float(third_value_str) / 100  # Convert to float and divide by 100
            return third_value_float, output_lines
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None


class RewardProcessor:
    def __init__(self, jar_classpath="AML/AgreementMakerLight.jar"):

        """
        Initializes a Java Virtual Machine and loads a Java lib in Python.

        :param jar_classpath: specifies the name to the JAR file that contains
            the Java classes needed for the code to run.
        """
        # Check if a JVM is already running.
        if not jpype.isJVMStarted():
            # Start the JVM with the specified classpath
            jpype.startJVM(jpype.getDefaultJVMPath(), classpath=jar_classpath)
        self.aml = JPackage("aml").AML.getInstance()
        self.aml.openOntologies("AML/store/anatomy/human.owl", "AML/store/anatomy/mouse.owl")
        self.aml.openReferenceAlignment("AML/store/anatomy/reference.rdf")

        # Load the Java class

    def execute(self, config: list):
        ArrayList = JClass('java.util.ArrayList')
        java_list = ArrayList()
        for item in config:
            java_list.add(item)

        self.aml.readConfigArray(java_list)
        self.aml.matchManual()
        self.aml.evaluate()
        output = self.aml.getEvaluation()
        return float(self.java_output_to_dict(str(output))['F-measure'].replace('%', '')) / 100

    def java_output_to_dict(self, evaluation):
        """

        :return:
        """
        lines = evaluation.strip().split('\n')

        # Extract header and data
        header = lines[0].split('\t')
        data = lines[1].split('\t')

        # Construct the dictionary
        result = {}
        for i in range(len(header)):
            result[header[i]] = data[i]
        return result

    def __del__(self):
        # Shutdown the JVM when the object is deleted
        jpype.shutdownJVM()
