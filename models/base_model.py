#!/usr/bin/python3
import models
from uuid import uuid4
from datetime import datetime

"""
This module defines the BaseModel class which defines all common attr/methods
of other classes
"""


class BaseModel:
    """
    BaseModel Class
    __init__ Creates new instance if no args otherwise
    recreate object from dict
    Args:
        args (list): Positional arguments
        kwargs (dict): Keyword arguments
    """

    def __eq__(self, other):
        if isinstance(other, dict):
            if self.to_dict() == other:
                return True
            return False
        else:
            if self.to_dict() == other.to_dict():
                return True
            return False

    def __init__(self, *args, **kwargs):
        """
        Create BaseModel object, or load from dict object
        Arguments:
            args (list): list (not used)
            kwargs (dict): dictionary
        """
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

        else:
            kwargs.pop('__class__')
            for k, v in kwargs.items():
                if k in ["created_at", "updated_at"]:
                    v = datetime.fromisoformat(v)
                setattr(self, k, v)

    def __str__(self):
        """
        String representation of Base class
        Returns:
            String representation of Base class
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Update attribute updated_at with current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Convert class object to dictionary
        Returns:
            Dictionary representation of class instance
        """
        # bm_dict ; base_model_dict
        bm_dict = {k: v for k, v in self.__dict__.items() if v is not None}
        bm_dict["__class__"] = self.__class__.__name__

        # isoformat() == strftime("%Y-%m-%dT%H:%M:%S.%f")
        bm_dict["created_at"] = bm_dict["created_at"].isoformat()
        bm_dict["updated_at"] = bm_dict["updated_at"].isoformat()

        return bm_dict
