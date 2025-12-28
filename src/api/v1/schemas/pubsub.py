from pydantic import BaseModel, Field

class PubSubData(BaseModel):
    data: str = Field(..., description="Pubsub Data")

class PubSubRead(BaseModel):
    message: PubSubData = Field(..., description="Pubsub Top Level Message")
    subscription: str = Field(..., description="Pubsub Top Level Message")

class PubSubRead(BaseModel):
    message: PubSubData = Field(..., description="Pubsub Top Level Message")
    subscription: str = Field(..., description="Pubsub Top Level Message")

class PubSubCreate(BaseModel):
    status: str = Field(..., description="Pubsub Top Level Message")