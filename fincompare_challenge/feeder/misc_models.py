import json
import re

EMAIL_REGEX = r'[^@]+@[^@]+\.[^@]+'


class ContactData:
    def __init__(self, name, email):
        if not re.match(EMAIL_REGEX, email):
            raise ValueError(f'Email: {email} has not a valid format.')
        self.email = email
        self.name = str(name)

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(data):
        data = json.loads(data)
        if 'email' not in data or 'name' not in data:
            raise Exception(f'The date could not convert to a Contact Data')

        return ContactData(name=data['name'], email=data['email'])
