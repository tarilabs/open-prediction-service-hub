#!/usr/bin/env python3
#
# Copyright 2020 IBM
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.IBM Confidential
#


import pickle
import typing

import sqlalchemy.orm as orm

import app.core.supported_lib as supported_lib
import app.crud as crud
import app.schemas as schemas
import app.models as models


def test_create_binary_ml_model(
    db: orm.Session,
    endpoint_in_db: models.Endpoint,
    classification_predictor: object
) -> typing.NoReturn:
    binary_in = schemas.BinaryMlModelCreate(
        model_b64=pickle.dumps(classification_predictor),
        library=supported_lib.MlLib.SKLearn
    )
    binary = crud.binary_ml_model.create_with_endpoint(db, obj_in=binary_in, endpoint_id=endpoint_in_db.id)

    assert binary.endpoint_id == endpoint_in_db.id
    assert type(pickle.loads(binary.model_b64)) == type(classification_predictor)
    assert binary.library == supported_lib.MlLib.SKLearn


def test_get_binary_ml_model(
    db: orm.Session,
    endpoint_in_db: models.Endpoint,
    classification_predictor: object
) -> typing.NoReturn:
    binary_in = schemas.BinaryMlModelCreate(
        model_b64=pickle.dumps(classification_predictor),
        library=supported_lib.MlLib.SKLearn
    )
    binary = crud.binary_ml_model.create_with_endpoint(db, obj_in=binary_in, endpoint_id=endpoint_in_db.id)
    binary_1 = crud.binary_ml_model.get(db, id=binary.id)

    assert type(pickle.loads(binary_1.model_b64)) == type(classification_predictor)
    assert binary_1.library == binary.library


def test_get_binary_ml_model_by_endpoint(
    db: orm.Session,
    endpoint_in_db: models.Endpoint,
    classification_predictor: object
) -> typing.NoReturn:
    binary_in = schemas.BinaryMlModelCreate(
        model_b64=pickle.dumps(classification_predictor),
        library=supported_lib.MlLib.SKLearn
    )
    binary = crud.binary_ml_model.create_with_endpoint(db, obj_in=binary_in, endpoint_id=endpoint_in_db.id)
    binary_1 = crud.binary_ml_model.get_by_endpoint(db, endpoint_id=endpoint_in_db.id)

    assert type(pickle.loads(binary_1.model_b64)) == type(classification_predictor)
    assert binary_1.library == binary.library


def test_delete_binary_ml_model(
    db: orm.Session,
    endpoint_in_db: models.Endpoint,
    classification_predictor: object
) -> typing.NoReturn:
    binary_in = schemas.BinaryMlModelCreate(
        model_b64=pickle.dumps(classification_predictor),
        library=supported_lib.MlLib.SKLearn
    )
    binary = crud.binary_ml_model.create_with_endpoint(db, obj_in=binary_in, endpoint_id=endpoint_in_db.id)
    binary_1 = crud.binary_ml_model.delete(db, id=binary.id)
    binary_2 = crud.binary_ml_model.get(db, id=binary.id)

    assert binary_2 is None
    assert binary_1.id == binary.id
    assert type(pickle.loads(binary_1.model_b64)) == type(classification_predictor)
    assert binary_1.library == binary.library
