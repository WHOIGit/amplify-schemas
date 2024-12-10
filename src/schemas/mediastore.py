from typing import List, Dict, Optional, Union
from pydantic import BaseModel as Schema


### MEDIASTORE mediastore module ###

## Login Schemas ##

class LoginInputDTO(Schema):
    username: str
    password: str

class TokenOutputDTO(Schema):
    token: str

class ErrorDTO(Schema):
    error: str


## S3Config ##

class S3ConfigSchemaCreate(Schema):
    url: str
    access_key: str
    secret_key: str

class S3ConfigSchemaSansKeys(Schema):
    pk: int
    url: str


## StoreConfig ##

class StoreConfigSchemaCreate(Schema):
    type: str
    bucket: str
    s3_url: Optional[str] = ''

class StoreConfigSchema(StoreConfigSchemaCreate):
    pk: int


## Identifiers ##

class IdentifierTypeSchema(Schema):
    name: str
    pattern: Optional[str] = ''


## Media ##

class MediaSchema(Schema):
    pk: int
    pid: str
    pid_type: str
    mark: int
    version: str
    store_config: StoreConfigSchema
    store_status: str
    identifiers: dict
    metadata: dict
    tags: List[str] = []

class MediaSchemaCreate(Schema):
    pid: str
    pid_type: str
    store_config: StoreConfigSchemaCreate
    identifiers: Optional[Dict[str,str]] = {}
    metadata: Optional[dict] = {}
    tags: Optional[List[str]] = []

class MediaSchemaUpdate(Schema):
    pid: Optional[str] = None
    new_pid: Optional[str] = None
    pid_type: Optional[str] = None
    store_config: Optional[Union[int,StoreConfigSchemaCreate]] = None

class MediaSchemaUpdateTags(Schema):
    pid: str
    tags: List[str]

class MediaSchemaUpdateStorekey(Schema):
    pid: str
    store_key: str

class MediaSchemaUpdateIdentifiers(Schema):
    pid: str
    identifiers: Dict[str,str]

class MediaSchemaUpdateMetadata(Schema):
    pid: str
    keys: Optional[List[str]] = []
    data: Optional[Union[dict,list]] = {}

class MediaErrorSchema(Schema):
    pid: str
    error: str
    msg: str

class BulkUpdateResponseSchema(Schema):
    successes: list[str]
    failures: list[MediaErrorSchema]

class MediaSearchSchema(Schema):
    tags: list[str]
    # TODO other search vectors


### MEDIASTORE file_handler module ###

## Upload Schemas ##
class UploadSchemaInput(Schema):
    mediadata: MediaSchemaCreate
    base64: Optional[str] = ''

class UploadSchemaOutput(Schema):
    status: str
    presigned_put: Optional[str] = None

class UploadError(Schema):
    error: str

## Download Schemas ##
class DownloadSchemaInput(Schema):
    pid: str
    direct: Optional[bool] = True

class DownloadSchemaOutput(Schema):
    mediadata: MediaSchema
    base64: Optional[str] = ''
    presigned_get: Optional[str] = ''

