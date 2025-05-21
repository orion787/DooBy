from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, String, ForeignKey

def StringField(length=255):
    return Column(String(length))

def IntegerField():
    return Column(Integer)

def FloatField():
    return Column(Float)

def DateTimeField():
    return Column(DateTime)

def KeyField():
    return Column(Integer, primary_key=True)

def RefTo(ref_to, parrent):
    return relationship(ref_to, back_populates=parrent)


def ExternalKey(key):
    return Column(Integer, ForeignKey(key))
