#include <cstdint>
#include <cstring>
#include "serializer.h"

class SerializerBytes : public Serializer {
public:
  template <typename T>
  static void deserialize(std::vector<uint8_t>& data, const T& object) {
    // check data size

    std::memcpy(data.data(), &object, sizeof(T));
  }
  template <typename T>
  void serialize(std::vector<uint8_t>& result, const T& data) {
    const uint8_t* bytes = reinterpret_cast<const uint8_t*>(&data);
    result.insert(result.end(), bytes, bytes + sizeof(T));
  }
};