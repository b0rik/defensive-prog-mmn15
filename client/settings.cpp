#include <string>
#include <fstream>
#include "settings.h"

const int ADDRESS_LINE = 1;
const int NAME_LINE = 2;
const int FILE_PATH_LINE = 3;
const int USER_NAME_LINE = 1;
const int ID_LINE = 2;
const int KEY_LINE = 3;

Settings::Settings(std::string info_file, std::string user_file) 
  : info_file(info_file)
  , user_file(user_file) {
  this->file_path = read_file_path();
  this->address = read_address();
  this->name = read_name();
  this->id = read_id();
  this->key = read_key();
}

std::string get_line(std::fstream &fs, int line_num) {
  std::string line;

  for(int i = 0; i < line_num; i++) {
    std::getline(fs, line);
  }

  return line;
}

std::string Settings::read_file_path() {
  std::fstream fs;

  fs.open(this->info_file, std::fstream::in);
  std::string file_path = get_line(fs, FILE_PATH_LINE);
  fs.close();

  return file_path;
}

std::string Settings::read_address() {
  std::fstream fs;

  fs.open(this->info_file, std::fstream::in);
  std::string address = get_line(fs, ADDRESS_LINE);
  fs.close();

  return address;
}

std::string Settings::read_name() {
  std::fstream fs;
  std::string name;

  fs.open(this->user_file, std::fstream::in);
  if(!fs.good()) {
    fs.open(this->info_file, std::fstream::in);
    name = get_line(fs, NAME_LINE);
    fs.close();
    return name;
  }

  name = get_line(fs, USER_NAME_LINE);
  fs.close();

  return name;
}

std::string Settings::read_id() {
  std::fstream fs;
  std::string id;

  fs.open(this->user_file, std::fstream::in);
  if(!fs.good()) {
    return "";
  }

  id = get_line(fs, ID_LINE);
  fs.close();

  return id;
}

std::string Settings::read_key() {
  std::fstream fs;
  std::string key;

  fs.open(this->user_file, std::fstream::in);
  if(!fs.good()) {
    return "";
  }

  key = get_line(fs, KEY_LINE);
  fs.close();

  return key;
}

std::string Settings::get_file_path() {
  return this->file_path;
}

std::string Settings::get_address() {
  return this->address;
}

std::string Settings::get_name() {
  return this->name;
}

std::string Settings::get_id() {
  return this->id;
}

std::string Settings::get_key() {
  return this->key;
}

void Settings::set_file_path(std::string file_path) {
  this->file_path = file_path;
}

void Settings::set_address(std::string address) {
  this->address = address;
}

void Settings::set_name(std::string name) {
  this->name = name;
}

void Settings::set_id(std::string id) {
  this->id = id;
}

void Settings::set_key(std::string key) {
  this->key = key;
}

bool Settings::id_exists() {
  return !this->id.empty();
}
