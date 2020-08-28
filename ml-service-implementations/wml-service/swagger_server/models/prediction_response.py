# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class PredictionResponse(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, result: Dict=None):  # noqa: E501
        """PredictionResponse - a model defined in Swagger

        :param result: The result of this PredictionResponse.  # noqa: E501
        :type result: Dict
        """
        self.swagger_types = {
            'result': Dict
        }

        self.attribute_map = {
            'result': 'result'
        }
        self._result = result

    @classmethod
    def from_dict(cls, dikt) -> 'PredictionResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PredictionResponse of this PredictionResponse.  # noqa: E501
        :rtype: PredictionResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def result(self) -> Dict:
        """Gets the result of this PredictionResponse.

        Result of a prediction  # noqa: E501

        :return: The result of this PredictionResponse.
        :rtype: Dict
        """
        return self._result

    @result.setter
    def result(self, result: Dict):
        """Sets the result of this PredictionResponse.

        Result of a prediction  # noqa: E501

        :param result: The result of this PredictionResponse.
        :type result: Dict
        """

        self._result = result
