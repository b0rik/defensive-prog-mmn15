DEFAULT_PORT = 1357
PORT_RANGE = (0, 65536)
PORT_FILE = 'port.info'
def get_port():
  try:
    with open(PORT_FILE, 'r') as file:
      port = file.read()
      if not port.isdigit() or int(port) not in range(*PORT_RANGE):
        raise ValueError
      return int(port)
  except FileNotFoundError:
    print(f'{PORT_FILE} file not found. using default port.')
  except ValueError:
    print(f'{PORT_FILE} file contains invalid port. Using default port.')
  
  return DEFAULT_PORT
