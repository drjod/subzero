
# NICHT VERWENDET

# Parameter für Stufenfunktion (Zyklusdauer und Belade bzw- Endtladerate)
# Wärmbeladung (value positiv) und Wärmeentladung (value negativ) im Wechsel
class SourceTerm:
    def __init__(self,
                 cylce_duration,  # [s], z.B. ein Jahr: 31536000
                 value  # Belade- und Entladerate [W], positiv: Start mit Beladung
                 ):
        self.__cycle_duration = cylce_duration
        self.__value = value
    @property
    def cylce_duration(self):
        return self.__cycle_duration
    @property
    def value(self):
        return self.__value
