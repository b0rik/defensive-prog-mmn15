from abc import ABC, abstractmethod

class ParserInterface(ABC):
  @abstractmethod
  def parse(self, data):
    pass

  def get_parsed_payload(self):
    return self.paylaod