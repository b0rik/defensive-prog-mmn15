#include <fstream>
#include <filesystem>
#include <string>
#include "file_wrapper.h"

std::string file_wrapper::get_line_from_file(size_t line_num, const std::string& file_name) {
    std::ifstream fs(file_name);

    if (fs.is_open()) {
        std::string line;
        size_t curr_line = 0;
           
        // skip to line line_num 
        while (std::getline(fs, line)) {
            if (++curr_line == line_num) {
                fs.close();
                return line;
            }
        }
    }
    else {
        throw std::exception(std::string("failed to open file " + file_name).c_str());
    }

    fs.close();
    return "";
}

bool file_wrapper::file_exists(const std::string& file_name) {
    return std::filesystem::exists(file_name);
}

std::string file_wrapper::get_file(const std::string& file_name) {
    std::ifstream fs(file_name, std::ios::binary);
    std::string file_content;
    char buffer[file_wrapper::BUFFER_SIZE];

    if (fs.is_open()) {
        while (!fs.eof()) {
            fs.read(buffer, file_wrapper::BUFFER_SIZE);
            file_content.insert(file_content.end(), buffer, buffer + fs.gcount());
        }
        fs.close();
        return file_content;
    }
    else {
        throw std::exception(std::string("failed to open file" + file_name).c_str());
    }
}

void file_wrapper::add_to_file(const std::string& file_name, const std::string& data) { 
    std::ofstream fs(file_name, std::ios::app);

    if (fs.is_open()) {
        fs << data << std::endl;
        fs.close();
    }
    else {
        throw std::exception(std::string("failed to open file" + file_name).c_str());
    }
}

std::string file_wrapper::get_file_from_line(const std::string& file_name, const size_t line_num) {
    std::ifstream fs(file_name);
    std::string file_content;
    char buffer[file_wrapper::BUFFER_SIZE];

    if (fs.is_open()) {
        std::string line;
        size_t curr_line = 1;

        // skip lines up to line line_nu,
        while (curr_line < line_num && std::getline(fs, line)) {
            ++curr_line;
        }
        
        // read from line line_num
        while (!fs.eof()) {
            fs.read(buffer, file_wrapper::BUFFER_SIZE);
            file_content.insert(file_content.end(), buffer, buffer + fs.gcount());
        }

        fs.close();
        return file_content;
    }
    else {
        throw std::exception(std::string("failed to open file" + file_name).c_str());
    }
}

void file_wrapper::reset_file(const std::string& file_name) {
    if (file_wrapper::file_exists(file_name)) {
        std::ofstream fs(file_name);
        fs << "";
        fs.close();
    }
}