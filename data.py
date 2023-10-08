import json
import auth
import datetime

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
USERS = {'1': User('1', auth.username)}

class Tables():
    def __init__(self):
        self.info = json.load( open( "/root/Prella/save_info.json" ) )
        self.order = json.load( open( "/root/Prella/save_order.json" ) )
        if len(self.order) == 0: 
            self.new_id_table = 0
        else:
            self.new_id_table = max(map(int, self.order)) + 1
        

    def saveData(self):
        json.dump(self.info, open( "/root/Prella/save_info.json", 'w' ))
        json.dump(self.order, open( "/root/Prella/save_order.json", 'w' ))
        json.dump(self.info, open( "/root/Prella/backup/save_info"+str(datetime.datetime.now())+".json", 'w' ))
        json.dump(self.order, open( "/root/Prella/backup/save_order"+str(datetime.datetime.now())+".json", 'w' ))
     
    def create_table(self, label):
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
    
    def create_task(self, label, table_id):
        if type(table_id) != str:
            table_id = str(table_id)
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
    
    def delete_table(self, table_id):
        if type(table_id) != str:
            table_id = str(table_id)
        if table_id in self.order and table_id in self.info.keys():
            del self.order[self.order.index(table_id)]
            return self.info.pop(table_id)
        else:
            return 'error'
    
    def delete_task(self, id, table_id):
        if type(table_id) != str:
            table_id = str(table_id)
        if type(id) != str:
            id = str(id)
        if table_id in self.info.keys() and id in self.info[table_id]['tasks_order'] and id in self.info[table_id]['tasks_info'].keys():
            del self.info[table_id]['tasks_order'][self.info[table_id]['tasks_order'].index(id)]
            return self.info[table_id]['tasks_info'].pop(id)
        else:
            return 'error'
    
    def rename_table(self, table_id, label):
        if type(table_id) != str:
            table_id = str(table_id)
        if table_id in self.info.keys():
            if self.info[table_id]['label'] == label:
            	return 'same'
            else:
            	self.info[table_id]['label'] = label
            	return 1
        else:
            return 'error'
    
    def rename_task(self, id, table_id, label):
        if type(table_id) != str:
            table_id = str(table_id)
        if type(id) != str:
            id = str(id)
        try:
            if self.info[table_id]['tasks_info'][id]['label'] == label:
                return 'same'
            self.info[table_id]['tasks_info'][id]['label'] = label
        except:
            return 'error'
    
    def changeIndexTable(self, table_id, oldIndex, newIndex):
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
    
    def changeIndexTask(self, task_id, oldIndex, newIndex, toTable, fromTable):
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