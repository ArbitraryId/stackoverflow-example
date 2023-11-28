import uuid

from pydantic import UUID4, BaseModel
from typing import List


class DynamicEnumValue(BaseModel):
    key: str
    value: str
    description: str
    order: int


class DynamicEnum(BaseModel):
    enum_id: UUID4
    name: str = ""
    values: List[DynamicEnumValue] = []

    @staticmethod
    async def get_all():
        enums = [{
            "enum_id": uuid.uuid4(),
            "name": "Enum1",
            "values": [
                {
                "key": "TestKey1",
                "value": "test",
                "description": "This is the first test value",
                "order": 0
                },
                {
                "key": "TestKey2",
                "value": "test2",
                "description": "This is the second test value",
                "order": 1
                },
                {
                "key": "TestKey3",
                "value": "test3",
                "description": "This is the third test value",
                "order": 2
                }
            ]
        }]

        return [DynamicEnum.parse_obj(enum) for enum in enums]
