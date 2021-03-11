from .Punto import Punto

class Intersection:
  def __init__(self, segments, point=Punto()):
    self.point = point
    self.segments = segments
  def __repr__(self):
    return f"{self.point} -> {[segment.name for segment in self.segments]}"
