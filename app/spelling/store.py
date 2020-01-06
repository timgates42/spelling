"""
Storage Handling for spelling
"""

import json

import dataset


class StorageHandler(object):
    """
    Simple dataset json storage
    """

    def __init__(self, storage_path):
        self.con = self.get_db(storage_path)
        self.table = self.con["storage"]

    @staticmethod
    def get_db(storage_path):
        """
        dataset storage
        """
        if storage_path is None:
            return dataset.connect("sqlite:///:memory:")
        return dataset.connect(f"sqlite:///{storage_path}")

    def load_word_count(self):
        """
        Retrieve json word count
        """
        table = self.table
        row = table.find_one(name="word_count")
        if not row:
            return {}
        return json.loads(row["value"])

    def save_word_count(self, value):
        """
        Save json word count
        """
        table = self.table
        table.upsert({"name": "word_count", "value": json.dumps(value)}, keys=["name"])


def get_store(storage_path):
    """
    Return the dataset handler for storing details.
    """
    return StorageHandler(storage_path)
