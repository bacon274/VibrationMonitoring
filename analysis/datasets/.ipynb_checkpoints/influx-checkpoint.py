import tomli
import influxdb_client
import torch
from torch.utils.data import Dataset, DataLoader


def get_config():
    with open("./config.toml", "rb") as f:
        toml_conf = tomli.load(f)
    logger.info(f"config:{toml_conf}")
    return toml_conf

# Custom dataset for InfluxDB data
class InfluxDBDataset(Dataset):
    def __init__(self, influxdb_data):
        self.data = influxdb_data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data[idx]
        # Perform any necessary data preprocessing here
        # Return data as PyTorch tensors
        return torch.tensor(sample, dtype=torch.float32),  # Comma to return a tuple



class InfluxData(): 
    def __init__(self, config):
        self.config = config
        self.influxdb = influxdb_client.InfluxDBClient(
            url=config['influxdb']['url'],
            token=config['influxdb']['token'],
            org=config['influxdb']['org'],
            debug=config['influxdb']['debug'],
        )
        self.bucket = config['influxdb']['bucket']
        self.query_api = self.influxdb.query_api()
        self.query = f'from(bucket: "{self.bucket}") |> range(start: -1h)'
        self.tables = self.query_api.query(query=self.query)
        self.data = []
        for table in self.tables:
            for row in table.records:
                self.data.append(row.values)
        self.dataset = InfluxDBDataset(self.data)
        self.dataloader = DataLoader(self.dataset, batch_size=32, shuffle=True)

    def get_data(self):
        return self.data

    def get_dataset(self):
        return self.dataset

    def get_dataloader(self):
        return self.dataloader

    def get_config(self):
        return self.config

    def get_influxdb(self):
        return self.influxdb

    def get_bucket(self):
        return self.bucket

    def get_query_api(self):
        return self.query_api

    def get_query(self):
        return self.query

    def get_tables(self):
        return self.tables

    def set_data(self, data):
        self.data = data

    def set_dataset(self, dataset):
        self.dataset = dataset

    def set_dataloader(self, dataloader):
        self.dataloader = dataloader

    def set_config(self, config):
        self.config = config

    def set_influxdb(self, influxdb):
        self.influxdb = influxdb

    def set_bucket(self, bucket):
        self.bucket = bucket

    def set_query_api(self, query_api):
        self.query_api = query_api

    def set_query(self, query):
        self.query = query

    def set_tables(self, tables):
        self.tables = tables

    def __str__(self):
        return f"""InfluxData(
    config={self.config},
    influxdb={self.influxdb},
    bucket={self.bucket},
    query_api={self.query_api},
    query={self.query},
    tables={self.tables},
    data={self.data},
    dataset={self.dataset},
