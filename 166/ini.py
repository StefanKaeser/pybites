import configparser
from contextlib import suppress


class ToxIniParser:
    def __init__(self, ini_file):
        """Use configparser to load ini_file into self.config"""
        self._config = configparser.ConfigParser()
        self._config.read(ini_file)

    @property
    def number_of_sections(self):
        """Return the number of sections in the ini file.
           New to properties? -> https://pybit.es/property-decorator.html
        """
        return len(self._config.sections())

    @property
    def environments(self):
        """Return a list of environments
           (= "envlist" attribute of [tox] section)"""
        env_string = self._config["tox"]["envlist"]
        env_list = env_string.replace("\n", ",").split(",")
        env_list = [string.strip() for string in env_list if string]
        return env_list

    @property
    def base_python_versions(self):
        """Return a list of all basepython across the ini file"""
        basepythons = set()
        for section in self._config.sections():
            with suppress(KeyError):
                basepythons.add(self._config[section]["basepython"])
        return list(basepythons)
