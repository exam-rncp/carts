import os
import unittest
from os.path import expanduser

from util.Docker import Docker

# Define default values for environment variables
default_values = {
    'COVERALLS_TOKEN': 'default_token',
    'TRAVIS_JOB_ID': '0',
    'TRAVIS_BRANCH': 'main',
    'TRAVIS_PULL_REQUEST': 'false',
    'TRAVIS': 'ci'
}

# Retrieve environment variables, falling back to default values
env_values = {key: os.getenv(key, default) for key, default in default_values.items()}

class JavaServices(unittest.TestCase):

    def test_maven(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        code_dir = script_dir + "/.."
        home = expanduser("~")
        command = ['docker', 'run', '--rm',
                   '-v', home + '/.m2:/root/.m2',
                   '-v', code_dir + ':/usr/src/mymaven',
                   '-w', '/usr/src/mymaven',
                   'maven:3.6-jdk-11'
                ]
        print("docker command: ",command)
        
        print(Docker().execute(command))


if __name__ == '__main__':
    unittest.main()
