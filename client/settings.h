#ifndef SETTINGS_H_
#define SETTINGS_H_

#include <string>
#include <cstdint>

const uint8_t VERSION = 1;

class Settings {
public:
  Settings(std::string info_file, std::string user_file);

  std::string get_file_path();
  std::string get_address();
  std::string get_name();
  std::string get_id();
  std::string get_key();

  void set_file_path(std::string file_path);
  void set_address(std::string address);
  void set_name(std::string name);
  void set_id(std::string id);
  void set_key(std::string key);

  bool id_exists();

private:
  std::string info_file;
  std::string user_file;
  std::string file_path;
  std::string address;
  std::string name;
  std::string id;
  std::string key;

  std::string read_file_path();
  std::string read_address();
  std::string read_name();
  std::string read_id();
  std::string read_key();
};

#endif // SETTINGS_H_