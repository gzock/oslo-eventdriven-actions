import os
import logging
import time

from oslo_config import cfg
import oslo_messaging

TRANSPORT_CONFIG = os.environ.get("TRANSPORT_CONFIG", "./transport.conf")

logger = logging.getLogger("oslo_messaging.notify.dispatcher")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s")

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)

class NotificationEndpoint(object):
  filter_rule = oslo_messaging.NotificationFilter(
    publisher_id=".*",
    event_type="compute.instance.*")

  def info(self, ctxt, publisher_id, event_type, payload, metadata):
   logger.info("target event detected. event payload: %s" % payload)

   ##################
   ## some actions ##
   ##################

   except:
     logger.exception("exception occured. ")
     return oslo_messaging.NotificationResult.HANDLED

  def warn(self, ctxt, publisher_id, event_type, payload, metadata):
    logger.info("[%s] [%s] [%s]" % (publisher_id, event_type, payload))
    return oslo_messaging.NotificationResult.HANDLED

  def error(self, ctxt, publisher_id, event_type, payload, metadata):
    logger.info("[%s] [%s] [%s]" % (publisher_id, event_type, payload))
    return oslo_messaging.NotificationResult.HANDLED

if __name__ == "__main__":
  transport = oslo_messaging.get_notification_transport(CONF)
  targets = [
    oslo_messaging.Target(topic="notifications", exchange="nova")
  ]
  endpoints = [
    NotificationEndpoint(),
  ]
  server = oslo_messaging.get_notification_listener(
              transport, targets, endpoints, allow_requeue=True,
              executor="threading", pool="oslo-eventdriven-action")

  try:
    logger.info("oslo-eventdriven-action started.")
    server.start()
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    logger.info("oslo-eventdriven-action stopping...")
    server.stop()
    server.wait()
