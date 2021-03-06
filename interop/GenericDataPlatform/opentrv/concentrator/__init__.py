# The OpenTRV project licenses this file to you
# under the Apache Licence, Version 2.0 (the "Licence");
# you may not use this file except in compliance
# with the Licence. You may obtain a copy of the Licence at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the Licence is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the Licence for the
# specific language governing permissions and limitations
# under the Licence.
#
# Author(s) / Copyright (s): Bruno Girin 2016

import logging
import argparse

import opentrv.concentrator.http
import opentrv.concentrator.mqtt

class Core(object):
    """
    The core of the concentrator code, where the MQTT source and HTTP sink
    components are created and connected and where the main loop is run.
    """

    def __init__(self, options):
        """
        Initialise the core of the system.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("Initialising core with options: "+str(options))
        self.options = options

    def run(self):
        """
        Run the main loop. This loop relies on the MQTT subscriber loop and
        exits when that loop exits.
        """
        self.logger.debug("Starting core")
        http_client =  opentrv.concentrator.http.Client(
            **self.options["http"])
        try:
            http_client.commission()
        except (Exception, ValueError) as e:
            self.logger.critical("Could not commission HTTP client, aborting:" + str(e))
            return
        mqtt_subscriber =  opentrv.concentrator.mqtt.Subscriber(
            sink=http_client, **self.options["mqtt"])
        mqtt_subscriber.start()


class OptionParser(object):
    """
    Object responsible for parsing command line options and presenting them
    in a structure that the core understands.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def parse(self, argv):
        self.logger.debug("Parsing command line options")
        options = {}
        parser = argparse.ArgumentParser(
            prog = self.__module__,
            description='''OpenTRV MQTT subscriber''')
        parser.add_argument(
            '-u', '--platform_url', default="http://localhost:5000",
            help="URL of the data platform.")
        parser.add_argument(
            '-s', '--mqtt_server', default="localhost",
            help='''MQTT server name.''')
        parser.add_argument(
            '-p', '--mqtt_port', type=int, default=1883,
            help='''MQTT port.''')
        parser.add_argument(
            '-t', '--mqtt_topic', default='OpenTRV/Local',
            help='''Root MQTT topic.''')
        parser.add_argument(
            '-c', '--mqtt_client', default='OpenTRV Bridge',
            help='''MQTT client ID.''')
        args = parser.parse_args()
        options["http"] = {
            "url": args.platform_url
        }
        options["mqtt"] = {
            "server": args.mqtt_server,
            "port": args.mqtt_port,
            "topic": args.mqtt_topic,
            "client": args.mqtt_client
        }
        return options
