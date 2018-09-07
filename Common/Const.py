# coding utf-8
# running state
NET_CLOSE = 0
NET_RUNNING = 1
NET_CONNECTING = 2

NET_STATE_STOP = 1


NET_STATE_STOP = 0				# state: init value
NET_STATE_CONNECTING = 1		# state: connecting
NET_STATE_ESTABLISHED = 2		# state: connected
NET_HEAD_LENGTH_SIZE = 4		# 4 bytes little endian (x86)
NET_HEAD_LENGTH_FORMAT = '<I'
NET_CONNECTION_NEW = 0			# new connection
NET_CONNECTION_LEAVE = 1		# lost connection
NET_CONNECTION_DATA = 2			# data coming

CONSOLE_OPEN = 0				# console open
CONSOLE_CLOSE = 1				# console close

