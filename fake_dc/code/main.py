# ----------------------------------------------------------------------
#
#    Temperature Monitoring (Basic solution) -- This digital solution enables, measures,
#    reports and records different  types of temperatures (ambient, process, equipment)
#    so that the temperature conditions surrounding a process can be understood and 
#    taken action upon. This version can work for 4 types of temperature sensors (now)
#    which include k-type, RTD, ambient (AHT20), and NIR-based sensors. 
#    The solution provides a Grafana dashboard that 
#    displays the temperature timeseries, set threshold value, and a state timeline showing 
#    the chnage in temperature. An InfluxDB database is used to store timestamp, temperature, 
#    threshold and status. 
#
#    Copyright (C) 2022  Shoestring and University of Cambridge
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see https://www.gnu.org/licenses/.
#
# ----------------------------------------------------------------------

# Check config file is valid
# create BBs
# plumb BBs together
# start BBs
# monitor tasks

# packages
import tomli
import time
import logging
import zmq
# local
import measure
import wrapper

logger = logging.getLogger("main")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # move to log config file using python functionality


def get_config():
    with open("./config/config.toml", "rb") as f:
        toml_conf = tomli.load(f)
    logger.info(f"config:{toml_conf}")
    return toml_conf


def config_valid(config):
    return True


def create_building_blocks(config):
    bbs = {}

    measure_out = {"type": zmq.PUSH, "address": "tcp://127.0.0.1:4000", "bind": True}
    wrapper_in = {"type": zmq.PULL, "address": "tcp://127.0.0.1:4000", "bind": False}

    bbs["measure"] = measure.TemperatureMeasureBuildingBlock(config, measure_out)
    bbs["wrapper"] = wrapper.MQTTServiceWrapper(config, wrapper_in)

    logger.debug(f"bbs {bbs}")
    return bbs


def start_building_blocks(bbs):
    for key in bbs:
        p = bbs[key].start()


def monitor_building_blocks(bbs):
    while True:
        time.sleep(1)
        for key in bbs:
            # logger.debug(f"{bbs[key].exitcode}, {bbs[key].is_alive()}")
            # todo actually monitor
            pass


if __name__ == "__main__":
    config = get_config()
    # todo set logging level from config file
    if config_valid(config):
        bbs = create_building_blocks(config)
        start_building_blocks(bbs)
        monitor_building_blocks(bbs)
    else:
        raise Exception("bad config")
