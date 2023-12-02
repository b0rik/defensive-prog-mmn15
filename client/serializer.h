#ifndef SERIALIZER_H_
#define SERIALIZER_H_

#include <vector>
#include <cstdint>
#include "message.h"

class Serializer {
public:
  virtual void serialize(std::vector<uint8_t>& result, const T& data) = 0;
  virtual static void deserialize(const std::vector<uint8_t>& bytes) = 0;
};

class SerializerBytes : public Serializer {
public:
  static void deserialize(std::vector<uint8_t>& data, const T& object);
  void serialize(std::vector<uint8_t>& result, const T& data);
};

#endif //SERIALIZER_H_