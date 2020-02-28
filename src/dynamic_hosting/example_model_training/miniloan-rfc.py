import logging
import sys

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
from time import gmtime, strftime
from os import path

from dynamic_hosting.core.model import MLModel


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger = logging.getLogger(__name__)

    names = ['name', 'creditScore', 'income', 'loanAmount', 'monthDuration', 'approval', 'rate', 'yearlyReimbursement']
    dtype = {
        'name': np.object,
        'creditScore': np.float64,
        'income': np.float64,
        'loanAmount': np.float64,
        'monthDuration': np.float64,
        'approval': np.object,
        'rate': np.float64,
        'yearlyReimbursement': np.float64
    }

    miniloan_dir = Path(path.abspath(__file__)).parents[3].joinpath('data', 'decisions-on-spark', 'data', 'miniloan')
    miniloan_file = miniloan_dir.joinpath('{dataset_name}.{extension}'.format(
        dataset_name='miniloan-decisions-ls-10K', extension='csv'))

    data = pd.read_csv(
        miniloan_file,
        header=0,
        delimiter=r'\s*,\s*',
        engine='python',
        names=names,
        dtype=dtype
    )

    data = data.replace([np.inf, -np.inf], np.nan).dropna()
    data = data.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'approval']]

    train, test = train_test_split(data, random_state=0)

    logger.info('training size: {size}'.format(size=len(train)))
    logger.info('validation size: {size}'.format(size=len(test)))

    grid = {
        'criterion': ['gini'],
        'n_estimators': [int(x) for x in np.linspace(50, 1000, num=20)],
        'min_samples_split': [int(x) for x in np.linspace(2, 64, num=50)],
        'min_samples_leaf': [int(x) for x in np.linspace(1, 32, num=20)]
    }

    hyper_tuning_params = {
        'estimator': RandomForestClassifier(random_state=0),
        'cv': 3,
        'verbose': bool(__debug__),
        'n_jobs': -1,
        'scoring': 'accuracy',
        'error_score': 'raise'
    }

    random_search = {
        'param_distributions': grid,
        'random_state': 42,
        'n_iter': 100
    }

    parameter_estimator = RandomizedSearchCV(**{**hyper_tuning_params, **random_search})

    x = train.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate']]
    y = train.loc[:, 'approval']

    parameter_estimator.fit(x, y)
    best_estimator = RandomForestClassifier(
        random_state=0,
        **parameter_estimator.best_params_
    )

    best_estimator.fit(x, y)

    res = best_estimator.score(test.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate']],
                               test.loc[:, 'approval'])
    logger.info('accuracy: ' + str(res))

    internal_model = MLModel(
        model=best_estimator,
        name='miniloan-rfc-RandomizedSearchCV',
        version='v0',
        method_name='predict',
        input_schema=[
            {
                'name': "creditScore",
                'order': 0,
                'type': 'float'
            },
            {
                'name': "income",
                'order': 1,
                'type': 'float'
            },
            {
                'name': "loanAmount",
                'order': 2,
                'type': 'float'
            },
            {
                'name': "monthDuration",
                'order': 3,
                'type': 'float'
            },
            {
                'name': "rate",
                'order': 4,
                'type': 'float'
            },
            {
                'name': "yearlyReimbursement",
                'order': 5,
                'type': 'float'
            }
        ],
        output_schema=None,
        metadata={
            'name': 'Loan payment classification',
            'author': 'ke',
            'date': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            'metrics': {
                'accuracy': res
            }
        }

    )

    storage_root = Path(Path(path.abspath(__file__))).parents[3].joinpath('example_models')
    internal_model.save_to_disk(storage_root=storage_root)


if __name__ == '__main__':
    main()