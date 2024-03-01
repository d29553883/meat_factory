import threading
import time


class MeatFactory:
    def __init__(self):
        # 初始肉品數量
        self.beef = 10
        self.pork = 7
        self.chicken = 5
        # 創建互斥鎖
        self.lock = threading.Lock()

    def process_meat(self, employee, meat_type, process_time):
        # 處理肉品的方法
        print(f"{employee} 在 {time.strftime('%Y-%m-%d %H:%M:%S')} 取得 {meat_type} ")
        time.sleep(process_time)
        print(f"{employee} 在 {time.strftime('%Y-%m-%d %H:%M:%S')} 處理完 {meat_type} ")

    def employee(self, name, meat_type, process_time):
        while True:
            # 取得互斥鎖，確保同時只有一個員工可以取肉
            self.lock.acquire()
            # 判斷是否還有該種類的肉品需要處理
            if meat_type == "牛肉" and self.beef > 0:
                self.beef -= 1
                self.lock.release()
                self.process_meat(name, meat_type, process_time)
            elif meat_type == "豬肉" and self.pork > 0:
                self.pork -= 1
                self.lock.release()
                self.process_meat(name, meat_type, process_time)
            elif meat_type == "雞肉" and self.chicken > 0:
                self.chicken -= 1
                self.lock.release()
                self.process_meat(name, meat_type, process_time)
            else:
                # 如果該種類的肉品已經處理完畢，釋放互斥鎖並退出循環
                self.lock.release()
                break

factory = MeatFactory()

employees = ["A", "B", "C", "D", "E"]
meats = [("牛肉", 1), ("豬肉", 2), ("雞肉", 3)]

thread_list = []
# 創建並啟動每個員工的線程
for employee in employees:
    for meat_type, process_time in meats:
        t = threading.Thread(target=factory.employee, args=(employee, meat_type, process_time))
        thread_list.append(t)
        t.start()

# 等待所有線程結束
for i in thread_list:
    i.join()

print("所有肉品已處理完畢")