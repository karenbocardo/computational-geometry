from .Punto import Punto

class Intersection:
  def __init__(self, segments, point=Punto()):
    self.point = point
    self.segments = segments
  def __repr__(self):
    res = f"{self.point} ->"
    for segment in self.segments:
        res += f" {segment}"
    return res
