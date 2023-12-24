#pragma once
#include <string>

namespace file_wrapper {
    const size_t BUFFER_SIZE = 1024;

    std::string get_line_from_file(size_t line, const std::string& file_name);
    bool file_exists(const std::string& file_name);
    std::string get_file(const std::string& file_name);
    void add_to_file(const std::string& file_name, const std::string& data);
    std::string get_file_from_line(const std::string& file_name, const size_t line_num);
    void reset_file(const std::string& file_name);
}
