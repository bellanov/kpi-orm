"""Datastore Client."""

import logging
import os
from multiprocessing import Pool

import google.auth
from google.cloud import ndb


# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger("store-asset-data")

# Authenticate
credentials, project_id = google.auth.default()
client = ndb.Client()

# Parallelization
WORKER_POOL = int(os.getenv("NUM_WORKERS"))
logger.info("WORKER POOL: %s workers", WORKER_POOL)

# Model
Schema = {"epoch": ndb.IntegerProperty(required=True), "close": ndb.FloatProperty(required=True)}


def ndb_asset_factory(ticker: str) -> dict:
    """Generate an Asset for a given ticker.
    Args:
        ticker: the ticker to create an object for (i.e., AAPL).
    Returns:
        An Asset dictionary initialized with the given ticker.
    """
    return type(ticker, (ndb.Model, object), Schema)


def add_metric(ndb_entity):
    """Store Asset information in Datastore.
    Args:
        ndb_entity: tuple containing Asset info (ticker, date, close)
    """
    ndb_asset = ndb_asset_factory(ndb_entity[0])
    logger.debug("Asset => %s", ndb_asset)
    asset = ndb_asset(close=ndb_entity[2], epoch=int(ndb_entity[1]))
    asset.put()


def execute_tasks() -> None:
    """Query and store relevant Ticker information from Yahoo Finance.
    Args:
        ticker: the ticker to create data for (i.e., AAPL).
    Returns:
        A list of the rows of data created.
    """
    metrics = [
        {
            'name': 'unit_tests',
            'desc': 'Unit Tests',
            'value': '0',
            'type': 'int|float|tuple'
        },
        {
            'name': 'integration_tests',
            'desc': 'Integration Tests',
            'value': '0',
            'type': 'int|float|tuple'
        },
        {
            'name': 'system_tests',
            'desc': 'System Tests',
            'value': '0',
            'type': 'int|float|tuple'
        },
        {
            'name': 'regression_tests',
            'desc': 'Regression Tests',
            'value': '0',
            'type': 'int|float|tuple'
        },
    ]
    with client.context():

        with Pool(WORKER_POOL) as pool:
            # Execute add_kpi() on all kpis in the list
            pool.map(add_metric, metrics)

