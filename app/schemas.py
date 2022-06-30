from pydantic import BaseModel

class Program(BaseModel): 
    title: str  
    network: str
    date: str
