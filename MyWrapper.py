from ibapi.wrapper import EWrapper

# Класс-наследник EWrapper
class MyWrapper(EWrapper):
    # Добавлен инициализатор объекта
    def __init__(self):
        self.nvid = 0                                            # Будем записывать Next Valid Identifier
        self.end_work_with_TWS = False                           # "Флаг" для отключения от TWS
 
    # Переписан базовый метод .error()
    def error(self, reqId:int, errorCode:int, errorString:str):
        if reqId != -1:                                          # Если это не ошибка из служебной информации при подключении
            print(f"[{reqId}] code: {errorCode} || {errorString}")# Печатаем ее
 
    # Переписан базовый метод .connectAck()
    def connectAck(self):
        print("connectAck(): connection established")           # "Принтуем", что метод сработал
 
    # Переписан базовый метод .nextValidId()
    def nextValidId(self, orderId:int):
        self.nvid = orderId                                      # Сохраняем Next Valid ID в собственный атрибут
        print("nextValidId(): new ID = {}".format(self.nvid))  # "Принтуем", что метод сработал
 
    # Переписан базовый метод .connectionClosed()
    def connectionClosed(self):
        print("connectionClosed(): terminal is disconnected")    # "Принтуем", что метод сработал
        self.end_work_with_TWS = True                            # Устанавливаем собственный флаг отключения от терминала