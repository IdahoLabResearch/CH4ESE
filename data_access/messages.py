"""
CH4ESE - Conversion Helper 4 Easy Serialization of EXI
Copyright 2024, Battelle Energy Alliance, LLC

This class is unused in the actual conversions, however the user can import the
class to store the messages it is receiving from the web server for further use.
"""

import xml.dom.minidom

# Helper class for Messages that is used to store the data for a single message
class Message:
    def __init__(self, format, data):
        self._data = data
        self._format = format

    def pretty_xml(self):
        try:
            xml_data = xml.dom.minidom.parseString(self._data)
            return xml_data.toprettyxml()
        except:
            return -1


# Messages class that can be used by to store multiple messages as the user is retrieving from the web server
class Messages:
    def __init__(self, format):
        self.format = format # 'XML' or 'EXI'
        self._messages = []

    async def add_message(self, data):
        message = Message(self.format, data)
        self._messages.append(message)

    def get_messages(self):
        return self._messages
