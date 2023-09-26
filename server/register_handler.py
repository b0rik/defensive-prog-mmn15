from handler import Handler

class RegisterHandler(Handler):
  def handle(self, request, **managers):
    name = request.get_payload().get_name()
    client = managers.get('clients_manager').get_client_by_name(name)

    if client:
      print(f'The name {name} is already registered.')
      pass # send response 2101

    succ_register = managers.get('clients_manager').register_client(name)
    if not succ_register:
      print(f'Error registering the client {name}')
      # send response 2101
      pass

    # send response 2100