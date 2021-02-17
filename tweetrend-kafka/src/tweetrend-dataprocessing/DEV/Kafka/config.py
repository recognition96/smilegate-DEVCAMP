import configparser
import sys
import os


class Config:
    def __init__(self, argv):
        if os.path.exists(argv) is False:
            print(f"{argv} file does not exist.")
            sys.exit(1)

        self.config_file = argv
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file, encoding='utf-8')

    def load_config(self, section: str, key: str):
        try:
            value = self.config[str(section)][str(key)]
        except AttributeError as e:
            print(f"AttributeError: type of section should be string.")
            sys.exit(1)
        except KeyError as e:
            print(f"KeyError: there is no section named {e} in the file.")
            sys.exit(1)
        return value


if __name__ == '__main__':
    config = Config([None, 'configs/kafka_config.conf'])
    print(config.load_config('TOPIC', 'covid_kr'))
