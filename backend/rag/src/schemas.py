from typing import List, Dict
from uuid import UUID

from pydantic import BaseModel


class PreparedToUpsertDocuments(BaseModel):
    ids: List[UUID]
    payloads: List[Dict]
    vectors: List[List[float]]
