class Modelo:
  """Clase para almacenar la configuración o modelación del sistema
  """
  def __init__(self, config):
    self.poblacion_inicial = config['pob_ini']
    self.poblacion_max = config['pob_max']
    self.objetivo_x = config['objetivo_x']
    self.objetivo_y = config['objetivo_y']

  def get_poblacion_inicial(self):
    return self.poblacion_inicial

  def get_poblacion_maxima(self):
    return self.poblacion_max

  def get_objetivo_x(self):
    return self.objetivo_x

  def get_objetivo_y(self):
    return self.objetivo_y