import json
import re

EMAIL_REGEX = r'[^@]+@[^@]+\.[^@]+'


class ContactData:
    def __init__(self, name, email):
        if not re.match(EMAIL_REGEX, email):
            raise Exception(f'Email: {email} has not a valid format.')
        self.email = email
        self.name = str(name)

    def to_json(self):
        return json.dumps(self.__dict__)