"""
  SERVER_STATUS:
  UNKNOWN - Wait client interface to provide initial value
  STANDBY - Ony to receive synchronize request and ready to pick up primary role
  PRIMARY - Primary server wo recvie requests from client
 """

class Globvar:
  _ONE_DAY_IN_SECONDS = 60 * 60 * 24
  SYNC_PORT = 50002
  ACTION_ID =
  # in terms of seconds
  CHECKPOINT_DURATION  = 15
  # in terms of seconds
  LIVE_CHECK_DURAITON = 30