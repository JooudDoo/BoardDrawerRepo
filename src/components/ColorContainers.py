from contextlib import suppress

class ColorContainer():
    def __init__():
        pass


class RGB(ColorContainer):
    """
    Класс содержащий значения RGB
    """
    name : str = "RGB"
    red : int = 0
    green : int = 0
    blue : int = 0

    def __init__(self, red = 0, green = 0, blue = 0, rgb = ()):
        self.color = None
        if rgb:
            self.red, self.green, self.blue = rgb[0], rgb[1], rgb[2]
        else:
            self.red, self.green, self.blue = red, green, blue
    
    def _updateColorByName(self, color : str, val):
        setattr(self, color, val)

    def __setattr__(self, name, val):
        """
        Обновляет поле в классе, а также сохрянет достоверность массива 'color'
        """
        object.__setattr__(self, name, val)
        if self.color != (self.red, self.green, self.blue):
            self.color = (self.red, self.green, self.blue)
        
    def __str__(self):
        return f"[R: {self.red}, G: {self.green}, B: {self.blue}]"
    
    def maximizedString(self):
        return f"[R: 255, G: 255, B: 255]"


class HSL(ColorContainer):
    """
    Класс содержащий значения HLS
    """
    name : str = "HSL"
    hue : int = 0
    saturation : int = 0
    lightness : int = 0

    def __init__(self, hue = 0, saturation = 0, lightness = 0, hsl = ()):
        self.color = None
        if hsl:
            self.hue, self.saturation, self.lightness = hsl[0], hsl[1], hsl[2]
        else:
            self.hue, self.saturation, self.lightness = hue, saturation, lightness
        
    
    def _updateColorByName(self, color : str, val):
        setattr(self, color, val)

    def __setattr__(self, name, val):
        """
        Обновляет поле в классе, а также сохрянет достоверность массива 'color'
        """
        object.__setattr__(self, name, val)
        if self.color != (self.hue, self.saturation, self.lightness):
            self.color = (self.hue, self.saturation, self.lightness)
        
    def __str__(self):
        return f"[H: {self.hue}, S: {self.saturation}, L: {self.lightness}]"
    
    def maximizedString(self):
        return f"[H: 255, S: 255, L: 255]"