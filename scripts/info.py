import sys

import dogecoinrpc
import sys, time

# address = 'AddressToSendCoinTo'
serverIP = '127.0.0.1'
serverPort = '22555'#44555'
user = 'dogecoinrpc'
password = ''#F8RQ81wDv4bWsUjWGtV4dccwshrHX7UsLpfJrB1RkUK4'

fee = 0.001


conn = dogecoinrpc.connect_to_remote(user, password, host=serverIP, port=serverPort)
print conn.getinfo()
