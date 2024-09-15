from dataclasses import dataclass
import re

from domain.exceptions.s3_url import InvalidS3URLException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class S3URL(BaseValueObject):
    value: str

    def validate(self):
        if not re.match(r'(^$|(http(s)?:\/\/)([\w-]+\.)+[\w-]+([\w- ;,.\/?%&=]*))', self.value):
            raise InvalidS3URLException(self.value)

    def as_generic_type(self) -> str:
        return self.value
