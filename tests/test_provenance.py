import pytest
from datetime import datetime, timezone, timedelta
import json
from typing import Dict, Any

from schemas.provenance import (
    NodeCreate, NodeResponse,
    RelationCreate, RelationResponse,
    ProvenanceRecord, ProvenanceResponse,
    ProvType, ProvVerb,
    BaseProvenanceModel
)

def make_utc_datetime(dt: datetime) -> datetime:
    """Helper to ensure datetime is UTC with 'Z' representation"""
    return dt.astimezone(timezone.utc).replace(tzinfo=timezone.utc)

def test_base_model_configuration():
    """Test BaseProvenanceModel configuration"""
    class TestModel(BaseProvenanceModel):
        required: str
        optional: str | None = None
        
    model = TestModel(required="test")
    serialized = json.loads(model.model_dump_json())
    assert "required" in serialized
    assert "optional" not in serialized

def test_node_create_serialization():
    """Test NodeCreate serialization with required and optional fields"""
    # Test with minimal required fields
    node = NodeCreate(
        label="test-node",
        node_type=ProvType.ENTITY,
    )
    serialized = json.loads(node.model_dump_json())
    assert serialized == {
        "label": "test-node",
        "node_type": "Entity",
        "metadata": {}
    }

    # Test with all fields
    node_full = NodeCreate(
        label="test-node-full",
        node_type=ProvType.ACTIVITY,
        description="Test description",
        metadata={"key": "value"}
    )
    serialized_full = json.loads(node_full.model_dump_json())
    assert serialized_full == {
        "label": "test-node-full",
        "node_type": "Activity",
        "description": "Test description",
        "metadata": {"key": "value"}
    }

def test_relation_create_serialization():
    """Test RelationCreate serialization with timestamps"""
    now = make_utc_datetime(datetime.now())
    later = make_utc_datetime(now + timedelta(hours=1))
    
    # Test with all optional fields
    relation = RelationCreate(
        subject_label="subject-node",
        verb=ProvVerb.WAS_GENERATED_BY,
        object_label="object-node",
        start_time=now,
        end_time=later,
        metadata={"key": "value"}
    )
    serialized = json.loads(relation.model_dump_json())
    assert serialized == {
        "subject_label": "subject-node",
        "verb": "wasGeneratedBy",
        "object_label": "object-node",
        "start_time": now.isoformat().replace("+00:00", "Z"),
        "end_time": later.isoformat().replace("+00:00", "Z"),
        "metadata": {"key": "value"}
    }

    # Test with minimal fields
    relation_minimal = RelationCreate(
        subject_label="subject-node",
        verb=ProvVerb.USED,
        object_label="object-node"
    )
    serialized_minimal = json.loads(relation_minimal.model_dump_json())
    assert serialized_minimal == {
        "subject_label": "subject-node",
        "verb": "used",
        "object_label": "object-node",
        "metadata": {}
    }

def test_provenance_record_serialization():
    """Test ProvenanceRecord serialization with nested objects"""
    nodes = [
        NodeCreate(
            label="node1",
            node_type=ProvType.ENTITY
        ),
        NodeCreate(
            label="node2",
            node_type=ProvType.ACTIVITY
        )
    ]
    
    relations = [
        RelationCreate(
            subject_label="node1",
            verb=ProvVerb.WAS_GENERATED_BY,
            object_label="node2"
        )
    ]
    
    record = ProvenanceRecord(
        nodes=nodes,
        relations=relations,
        run_id="test-run"
    )
    
    serialized = json.loads(record.model_dump_json())
    assert serialized == {
        "nodes": [
            {
                "label": "node1",
                "node_type": "Entity",
                "metadata": {}
            },
            {
                "label": "node2",
                "node_type": "Activity",
                "metadata": {}
            }
        ],
        "relations": [
            {
                "subject_label": "node1",
                "verb": "wasGeneratedBy",
                "object_label": "node2",
                "metadata": {}
            }
        ],
        "run_id": "test-run"
    }

def test_metadata_serialization():
    """Test that complex but valid metadata structures serialize correctly"""
    metadata = {
        "string": "value",
        "number": 42,
        "boolean": True,
        "null": None,
        "array": [1, 2, 3],
        "nested": {"key": "value"}
    }
    
    node = NodeCreate(
        label="test",
        node_type=ProvType.ENTITY,
        metadata=metadata
    )
    
    serialized = json.loads(node.model_dump_json())
    assert serialized["metadata"] == metadata