from ibapi.wrapper import EWrapper
import ibapi.contract

# Класс-наследник EWrapper
class MyWrapper(EWrapper):
    # Добавлен инициализатор объекта
    def __init__(self):
        self.nvid = 0                                            # Будем записывать Next Valid Identifier
        self.end_work_with_TWS = False                           # "Флаг" для отключения от TWS
        self.con_detail_recive = False                      # Флаг для полученного контракта
 
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

    # Метод, который принимает ответ на запрос деталей контракта
    def contractDetails(self, reqId:int, contractDetails: ibapi.contract.ContractDetails):
        # Выводим все параметры объекта и их значения
        for arg in dir(contractDetails):                    # Обходим все атрибуты объекта contractDetails
            if not arg.startswith('_'):                     # Исключаем приватные атрибуты
                val = getattr(contractDetails, arg)         # Значение конкретного атрибута
                print ("{} = {}".format(arg, val))          # Печатаем атрибут и его значение
    
    # Метод, завершающий прием ответа на запрос деталей контракта
    def contractDetailsEnd(self, reqId:int):
        self.con_detail_recive = True
        print("Закончили принимать параметры контракта")    # Печатаем статус
 
    # Переписан базовый метод .connectionClosed()
    def connectionClosed(self):
        print("connectionClosed(): terminal is disconnected")    # "Принтуем", что метод сработал
        self.end_work_with_TWS = True                            # Устанавливаем собственный флаг отключения от терминала