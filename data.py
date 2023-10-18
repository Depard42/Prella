import json
import datetime
import os

root_dir = os.path.split(os.path.abspath(__file__))[0]
backup_dir = os.path.join(root_dir, 'backup')
saves_dir = os.path.join(root_dir, 'saves')
saves_dir_order = os.path.join(saves_dir, "save_order.json")
saves_dir_info = os.path.join(saves_dir, "save_info.json")

def get_date():
    # Returns current date and time
    # In format '2023-Oct-09--03-44-39-021266'
    return datetime.datetime.now().strftime("%Y-%b-%d--%H-%M-%S-%f")

class User():
    def __init__(self, id, username):
        self.id = id
        self.username = 'test'
        self.active = True
    def is_active(self):
        return True
    def is_authenticated(self):
        return True
    def get_id(self):
        return self.id
USERS = {'1': User('1', os.environ['PRELLA_LOGIN'])}

class Tables():
    def __init__(self):
        if os.path.isfile(saves_dir_info) and os.path.isfile(saves_dir_order):
            print('!== Load exicting saves')
            self.info = json.load( open( saves_dir_info ) )
            self.order = json.load( open( saves_dir_order ) )
        else:
            print('!== No exicting saves, create blanc')
            self.info = {"last_task_id": 0}
            self.order = []
            self.saveData()
        if len(self.order) == 0: 
            self.new_id_table = 0
        else:
            self.new_id_table = max(map(int, self.order)) + 1
        

    def saveData(self):
        json.dump(self.info, open( saves_dir_info, 'w' ))
        json.dump(self.order, open( saves_dir_order, 'w' ))
        filename = get_date() + '.json'
        backup_info_dir = os.path.join(backup_dir, 'info#' +filename)
        backup_order_dir = os.path.join(backup_dir, 'oreder#' +filename)
        json.dump(self.info, open( backup_info_dir, 'w' ))
        json.dump(self.order, open( backup_order_dir, 'w' ))
     
    def create_table(self, label: str):
         id = str(self.new_id_table)
         if not id in self.order and not id in self.info.keys():
            self.new_id_table += 1
            self.info[id] = {'id':id, 
                            'label': label, 
                            'tasks_info': {}, 
                            'tasks_order':[]}
            self.order.append(id)
            return self.info[id]
         else:
            return 'error'
    
    def create_task(self, label: str, table_id: str):
        self.info["last_task_id"] += 1
        id = str(self.info["last_task_id"])
        if not id in self.info[table_id]['tasks_info'].keys() and not id in self.info[table_id]['tasks_order']:
            self.info[table_id]['tasks_info'][id] = {
                            'id':id, 
                            'label': label, 
                            'table_id': table_id}
            self.info[table_id]['tasks_order'].append(id)
            return self.info[table_id]['tasks_info'][id]
        else:
            return 'error'
    
    def delete_table(self, table_id: str):
        if table_id in self.order and table_id in self.info.keys():
            del self.order[self.order.index(table_id)]
            return self.info.pop(table_id)
        else:
            return 'error'
    
    def delete_task(self, id: str, table_id: str):
        if table_id in self.info.keys() and id in self.info[table_id]['tasks_order'] and id in self.info[table_id]['tasks_info'].keys():
            del self.info[table_id]['tasks_order'][self.info[table_id]['tasks_order'].index(id)]
            return self.info[table_id]['tasks_info'].pop(id)
        else:
            return 'error'
    
    def rename_table(self, table_id: str, label: str):
        if table_id in self.info.keys():
            if self.info[table_id]['label'] == label:
                return 'same'
            self.info[table_id]['label'] = label
            return 1
        else:
            return 'error'
    
    def rename_task(self, id: str, table_id: str, label: str):
        try:
            if self.info[table_id]['tasks_info'][id]['label'] == label:
                return 'same'
            self.info[table_id]['tasks_info'][id]['label'] = label
            return 1
        except:
            return 'error'
    
    def changeIndexTable(self, table_id: str, oldIndex, newIndex):
        try:
            if oldIndex != newIndex:
                self.order.remove(table_id)
                self.order.insert(newIndex, table_id)
                if newIndex + 1 == len(self.order):
                    next = 'end'
                else:
                    next = self.order[newIndex+1]
                return {'table_id': table_id, 'next': next}
        except:
            return 'error'
    
    def changeIndexTask(self, task_id: str, oldIndex, newIndex, toTable: str, fromTable: str):
        try:
            self.info[fromTable]['tasks_order'].remove(task_id)
            self.info[toTable]['tasks_order'].insert(newIndex, task_id)
            if toTable != fromTable:
                self.info[toTable]['tasks_info'][task_id] = self.info[fromTable]['tasks_info'][task_id]
                del self.info[fromTable]['tasks_info'][task_id]
            if newIndex + 1 == len(self.info[toTable]['tasks_order']):
                next = 'end'
            else:
                next = self.info[toTable]['tasks_order'][newIndex+1]
            return {'task_id': task_id, 'next': next, 'fromTable':fromTable, 'toTable': toTable}
        except:
            return 'error'

    def get_order(self):
        return self.order.copy()
    def get_info(self):
        return self.info.copy()