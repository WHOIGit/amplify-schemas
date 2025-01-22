from enum import Enum
import json
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Dict
from datetime import datetime, timezone


ISO_FORMAT='%Y-%m-%dT%H:%M:%S.%f%z'

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.astimezone(timezone.utc).strftime(ISO_FORMAT)
        return super().default(obj)


class BaseProvenanceModel(BaseModel):
    """Base model with UTC datetime configuration and JSON handling"""
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda dt: dt.astimezone(timezone.utc).strftime(ISO_FORMAT)
        },
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )
    
    def model_dump(self, *args, **kwargs):
        """Override model_dump to exclude None values by default"""
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)
        
    def model_dump_json(self, *args, **kwargs):
        """Override model_dump_json to exclude None values by default"""
        kwargs.setdefault("exclude_none", True)
        return super().model_dump_json(*args, **kwargs)

class ProvVerb(str, Enum):
    WAS_GENERATED_BY = "wasGeneratedBy"
    WAS_ATTRIBUTED_TO = "wasAttributedTo"
    WAS_ASSOCIATED_WITH = "wasAssociatedWith"
    USED = "used"
    ACTED_ON_BEHALF_OF = "actedOnBehalfOf"
    WAS_INFORMED_BY = "wasInformedBy"
    WAS_DERIVED_FROM = "wasDerivedFrom"
    WAS_REVISION_OF = "wasRevisionOf"
    WAS_QUOTED_FROM = "wasQuotedFrom"
    HAD_PRIMARY_SOURCE = "hadPrimarySource"
    WAS_STARTED_BY = "wasStartedBy"
    WAS_ENDED_BY = "wasEndedBy"
    INVALIDATED_BY = "invalidatedBy"
    WAS_INVALIDATED_BY = "wasInvalidatedBy"

    @classmethod
    def choices(cls):
        return [(verb.value, verb.name) for verb in cls]

class ProvType(str, Enum):
    ENTITY = "Entity"
    ACTIVITY = "Activity"
    AGENT = "Agent"
    BUNDLE = "Bundle"
    COLLECTION = "Collection"
    ORGANIZATION = "Organization"
    PERSON = "Person"
    SOFTWARE_AGENT = "SoftwareAgent"
    PLAN = "Plan"
    PRIMARY_SOURCE = "PrimarySource"
    REVISION = "Revision"
    QUOTATION = "Quotation"

    @classmethod
    def choices(cls):
        return [(type.value, type.name) for type in cls]

class NodeCreate(BaseProvenanceModel):
    label: str = Field(..., description="Globally unique identifier for the node")
    node_type: ProvType = Field(..., description="Type of provenance node")
    description: Optional[str] = Field(None, description="Human-readable description")
    metadata: Dict = Field(default_factory=dict, description="Additional attributes")

class RelationCreate(BaseProvenanceModel):
    subject_label: str = Field(..., description="Label of the subject node")
    verb: ProvVerb = Field(..., description="Type of provenance relationship")
    object_label: str = Field(..., description="Label of the object node")
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    metadata: Dict = Field(default_factory=dict, description="Additional attributes")

class ProvenanceRecord(BaseProvenanceModel):
    nodes: List[NodeCreate] = Field(..., description="Nodes to create if they don't exist")
    relations: List[RelationCreate] = Field(..., description="Relations to create between nodes")
    run_id: str = Field(..., description="Identifier for grouping related provenance statements")

class NodeResponse(BaseProvenanceModel):
    label: str = Field(..., description="Globally unique identifier for the node")
    node_type: ProvType = Field(..., description="Type of provenance node")
    description: Optional[str] = Field(None, description="Human-readable description")
    metadata: Dict = Field(default_factory=dict, description="Additional attributes")
    created_at: datetime = Field(..., description="When the node was first created")

class RelationResponse(BaseProvenanceModel):
    subject_label: str = Field(..., description="Label of the subject node")
    verb: ProvVerb = Field(..., description="Type of provenance relationship")
    object_label: str = Field(..., description="Label of the object node")
    run_id: str = Field(..., description="Identifier grouping related provenance statements")
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    metadata: Dict = Field(default_factory=dict, description="Additional attributes")
    created_at: datetime = Field(..., description="When the relation was created")

class ProvenanceResponse(BaseProvenanceModel):
    relations: List[RelationResponse] = Field(..., description="Relations created in this transaction")
