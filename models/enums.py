import re
import enum
import asyncio

from models.enum import DynamicEnum


class DynamicEnumCollection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DynamicEnumCollection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Avoid reinitialization
        if hasattr(self, '_initialized'):  
            return

        self.enums = {}
        self.enum_labels = {}
        self.enum_descriptions = {}
        self.enum_definitions = []
        self.loading = False
        self.loaded = False
        self._initialized = True

    def to_enum_key(self, text):
        if not text or text.isspace():
            return "Empty"

        enum_key = text.replace(" ", "_").replace("-", "_")
        enum_key = re.sub("[^0-9a-zA-Z_]", "", enum_key)

        # Remove more than one underscore in a row
        while "__" in enum_key:
            enum_key = enum_key.replace("__", "_")

        if enum_key[0].isdigit():
            enum_key = "_" + enum_key

        if enum_key[len(enum_key) - 1 :] == "_":
            enum_key = enum_key[: len(enum_key) - 1]

        if enum_key == "None":
            return "NONE"

        return enum_key

    async def load_definitions(self, global_import: bool = False):
        if self.loaded:
            return

        self.loading = True

        print("Loading enums...")

        enums = await DynamicEnum.get_all()

        print("Sorting enums...")
        enums = sorted(enums, key=lambda x: x.name)

        # Load definitions from API
        self.enum_definitions = enums 

        print("Importing enum definitions...")
        # Iterate definitions
        for e in self.enum_definitions:
            print(f"Enum Import: Loading {e.name}...")
            # Create enum type
            definition = enum.Enum(
                e.name,
                {self.to_enum_key(value.key): value.key for value in e.values},
            )

            # Map code labels
            self.enum_labels[e.name] = {
                value.key: value.value for value in e.values
            }

            # Map code descriptions
            self.enum_descriptions[e.name] = {
                value.key: value.description for value in e.values
            }

            # Store
            self.enums[e.name] = definition

            if global_import:
                globals()[e.name] = definition

        self.loaded = True
        self.loading = False

    def get_enum_definition(self, enum_name):
        if not self.loaded:
            if asyncio.get_event_loop().is_running():
                asyncio.create_task(self.load_definitions())
            else:
                asyncio.run(self.load_definitions())

        if enum_name not in self.enums:
            raise Exception(f"Could not find enum '{enum_name}'")

        return self.enums[enum_name]

    def get_key_label(self, enum_name, enum_key):
        # If no enum name has been given try to find the enum with the given key
        if enum_name is None:
            for e in self.enum_labels:
                if enum_key in self.enum_labels[e]:
                    return self.enum_labels[e][enum_key]

        if enum_name not in self.enum_labels:
            raise Exception(f"Could not find enum '{enum_name}'")

        if enum_key not in self.enum_labels[enum_name]:
            raise Exception(f"Could not find key '{enum_key}'")

        return self.enum_labels[enum_name][enum_key]

    def get_key_description(self, enum_name, enum_key):
        # If no enum name has been given try to find the enum with the given key
        if enum_name is None:
            for e in self.enum_descriptions:
                if enum_key in self.enum_descriptions[e]:
                    return self.enum_descriptions[e][enum_key]

        if enum_name not in self.enum_descriptions:
            raise Exception(f"Could not find enum '{enum_name}'")

        if enum_key not in self.enum_descriptions[enum_name]:
            raise Exception(f"Could not find key '{enum_key}'")

        return self.enum_descriptions[enum_name][enum_key]


enum_definitions = DynamicEnumCollection()
