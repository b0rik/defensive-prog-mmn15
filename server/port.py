DEFAULT_PORT = 1357
PORT_RANGE = (0, 65536)
def get_port():
  try:
    with open('port.info', 'r') as file:
      port = file.read()
      if not port.isdigit() or int(port) not in range(*PORT_RANGE):
        raise ValueError
      return int(port)
  except FileNotFoundError:
    print('port.info file not found. using default port.')
  except ValueError:
    print('port.info file contains invalid port. Using default port.')
  
  return DEFAULT_PORT
