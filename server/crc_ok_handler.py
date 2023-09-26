from handler import Handler

FILES_PATH = '/files'

class CRCOkHandler(Handler):
  def handle(self, request, **managers):
    client_id = request.get_header().get_client_id()
    file_name = request.get_payload().get_file_name()
    file_content = managers.get('files_manager').get_file_content_by_client_id_and_file_name(client_id, file_name)
    file_path = f'{FILES_PATH}/{client_id}/{file_name}'

    succ_set_crc = managers.get('files_manager').set_crc_ok(client_id, file_name)
    if not succ_set_crc:
      print(f'Error setting crc for file {file_name} from client {client_id}')
      # send response 2101

    try:
      with open(file_path, 'wb') as file:
        file.write(file_content)
    except Exception as e:
      print(f'Error writing file {file_name} from client {client_id}')
      # send response 2101

    # send response 2104