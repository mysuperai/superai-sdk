import os
from typing import List, Optional, Tuple


class EnvironmentFileProcessor:
    def __init__(self, location: str, filename: str = "environment"):
        self.location = location
        self.filename = filename
        if not self.location.endswith(self.filename):
            # update the path so that only self.location refers to environment file
            self.location = os.path.join(self.location, self.filename)
        self.environment_variables: dict = {}
        if not os.path.exists(self.location):
            self._write()
        else:
            self.environment_variables = self._read()

    @staticmethod
    def _process_input(
        input_str: str, value: Optional[str] = None, check_value: bool = True
    ) -> Tuple[str, Optional[str]]:
        """Helper to unify key, value
         - key: str, value: str is returned unchanged
         - key=value is returned as key: str, value: str

        You can perform a check if value is not None using check_value
        """
        if "=" in input_str:
            key, value = input_str.replace(" ", "").split("=")
        else:
            key = input_str
        if key is None or key == "":
            raise ValueError(f"Key cannot be {key} ({type(key)})")
        if value is None and check_value:
            raise ValueError(f"Value cannot be {value} ({type(value)})")
        return key, value

    def add_or_update(self, key: str, value: Optional[str] = None) -> None:
        """Add or update an environment variable."""
        key, value = self._process_input(key, value)
        self.environment_variables[key] = value
        self._write()

    def update_if_value_match(self, key: str, new_value: str, value: Optional[str] = None) -> None:
        """Update to new value only if key and value match"""
        if "=" not in key:
            if value is None:
                raise ValueError(f"Value cannot be {value} ({type(value)})")
        else:
            key, value = key.replace(" ", "").split("=")
        val = self.environment_variables[key]
        if val == value:
            self.environment_variables[key] = new_value
            self._write()

    def delete(self, key: str) -> None:
        """Delete an environment variable"""
        key, _ = self._process_input(key, check_value=False)
        if key in self.environment_variables:
            del self.environment_variables[key]
        self._write()

    def delete_if_value_match(self, key: str, value: Optional[str] = None) -> None:
        """Delete if value matches"""
        if "=" not in key:
            if value is None:
                raise ValueError("Need to pass value to check if value is same")
        else:
            key, value = key.replace(" ", "").split("=")
        val = self.environment_variables[key]
        if val == value:
            del self.environment_variables[key]
            self._write()

    def __contains__(self, key: str) -> bool:
        """Check if a key is present in the environment variables"""
        key, _ = self._process_input(key, check_value=False)
        return key in self.environment_variables.keys()

    def clear(self):
        """Deletes the existing environment file"""
        if os.path.exists(self.location):
            os.remove(self.location)
        self.environment_variables = {}
        self._write()

    def _env_str_list(self) -> List[str]:
        """Return environment variables in a list of string format separated by an '=' symbol"""
        return [f"{x}={y}" for x, y in self.environment_variables.items()]

    def _write(self) -> None:
        """Write environment file with the environment variables"""
        with open(self.location, "w") as env_file:
            env_file.write("\n".join(self._env_str_list()))

    def _read(self) -> dict:
        """Read already existing environment file and return dictionary of environment variables"""
        with open(self.location, "r") as env_file:
            content = env_file.read().split("\n")
        variables = {}
        for val in content:
            x, y = val.split("=")
            variables[x] = y
        return variables

    def from_dict(self, json_dict: dict) -> None:
        self.environment_variables = json_dict
        self._write()

    def to_dict(self) -> dict:
        return self.environment_variables
