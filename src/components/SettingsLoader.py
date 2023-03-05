import json

from components.ColorContainers import ColorContainer, RGB, HSL, colorFromStr


class ColorRangeSettings():

    def __init__(self, rangeType: str = None, minRange: ColorContainer = None, maxRange: ColorContainer = None):
        self.rangeType: str = rangeType
        if type(minRange) == str:
            self.minRange: ColorContainer = colorFromStr(self.rangeType, minRange)
            self.maxRange: ColorContainer = colorFromStr(self.rangeType, maxRange)
        else:
            self.minRange: ColorContainer = minRange
            self.maxRange: ColorContainer = maxRange

    def loadJSON(self, json):
        self.rangeType: str = json['rangeType']
        self.minRange: ColorContainer = json['minRange']
        self.maxRange: ColorContainer = json['maxRange']

    def getDict(self):
        return {"rangeType": self.rangeType, "minRange": str(self.minRange), "maxRange": str(self.maxRange)}

class DummySetting():
    def __init__(self, val):
        self.val = val
    
    def __call__(self, val):
        self.up(val)

    def up(self, val):
        self.val = val
    
    def getDict(self):
        return {'val': self.val}

class SettingsManager():
    """
    Класс содержащий менеджер настроек

    Отвечает за импортирование и экспортирование настроек в файл
    """

    """
    Это сетка методов генерации параметров
    В нее должны указываться какой класс отвечает за генерацию данного параметра по имени
    При `Импорте` будет подставлятся в его конструктор словарь
    При `Экспорте` будет использоваться метод getDict(), который должен вернуть словарь содержащий пары
        `имя_переменной` - значение (в форме строки)
    В рантайме можно добавить сюда метод генерации через addSetting
    """
    settingsGrid = {
        "ranges": ColorRangeSettings,
    }

    defaultSaveName = "cache"

    def __init__(self, settingsFile: str = None):
        self._settingList = []
        self.settingFile = settingsFile
        if settingsFile is None:
            settingsFile = self.defaultSaveName
        self.importSettingsFromJSON(self.settingFile)
        

    def updateSettingsInFile(self):
        self.exportSettingsToJSON(self.settingFile)

    def importSettingsFromJSON(self, filePath: str):
        with open(filePath, 'r', encoding='utf8') as f:
            try:
                settingsJSON = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                print(f"Couldn't read file: {filePath}")
                print(f"Create empty settings file: {filePath}_tmp")
                self.settingFile = filePath+"_tmp"
                with open(filePath+"_tmp", 'w', encoding='utf8') as f:
                    pass
                return
        self._settingList = []
        for key, value in settingsJSON.items():
            genMethod = self.settingsGrid.get(key, None)
            self.addSetting(key, value, genMethod)

    def exportSettingsToJSON(self, filePath: str):
        settingDict = dict()
        for setting in self.settingsList:
            try:
                settingData = self.getSetting(setting).getDict()
            except:
                settingData = self.getSetting(setting)
            settingDict.update({setting: settingData})
        with open(filePath, 'w', encoding='utf8') as saveFile:
            saveFile.write(json.dumps(settingDict, indent=2))

    def getSetting(self, settingName: str):
        try:
            return self.__getattribute__(settingName)
        except AttributeError:
            return None

    def addSetting(self, settingName: str, data, genMethod=None):
        """
        Параметры
        ---------
        `settingName` - имя настройки

        `data` - значение

        `genMethod` - класс для создания сложной настройки из JSON обьекта
            При `Импорте` будет подставлятся значения JSON обьекта в его конструктор, соответствуя полям

            При `Экспорте` будет использоваться метод getDict(), который должен вернуть словарь содержащий пары:
                `имя_переменной` - значение (в форме строки)
        Если 'genMethod` == None, будет использоватся оберка DummySetting
        """
        if settingName not in self._settingList:
            self._settingList.append(settingName)
        if genMethod is not None:
            self.settingsGrid.update({settingName: genMethod})
            self.__setattr__(settingName, genMethod(**data))
        else:
            self.settingsGrid.update({settingName: DummySetting})
            self.__setattr__(settingName, DummySetting(**data))

    @property
    def settingsList(self):
        return self._settingList

    def createSettingsDict(self, **kwargs):
        return kwargs
