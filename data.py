import json
import auth

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
        self.info = json.load( open( "save_info.json" ) )
        self.order = json.load( open( "save_order.json" ) )
        if len(self.order) == 0: 
            self.new_id_table = 0
        else:
            self.new_id_table = int(max(self.order))+1
        

    def saveData(self):
        json.dump(self.info, open( "save_info.json", 'w' ))
        json.dump(self.order, open( "save_order.json", 'w' ))
    
    def create_table(self, label):
        try:
            id = str(self.new_id_table)
            self.new_id_table += 1
            self.info[id] = {'id':id, 
                            'label': label, 
                            'tasks_info': {}, 
                            'tasks_order':[]}
            self.order.append(id)
            return self.info[id]
        except:
            return 'error'
    
    def create_task(self, label, table_id):
        if type(table_id) != str:
            table_id = str(table_id)
        try:
            self.info["last_task_id"] += 1
            id = str(self.info["last_task_id"])
            self.info[table_id]['tasks_info'][id] = {
                            'id':id, 
                            'label': label, 
                            'table_id': table_id}
            self.info[table_id]['tasks_order'].append(id)
            return self.info[table_id]['tasks_info'][id]
        except:
            return 'error'
    
    def delete_table(self, table_id):
        if type(table_id) != str:
            table_id = str(table_id)
        try:
            del self.order[self.order.index(table_id)]
            return self.info.pop(table_id)
        except:
            return 'error'
    
    def delete_task(self, id, table_id):
        if type(table_id) != str:
            table_id = str(table_id)
        if type(id) != str:
            id = str(id)
        try:
            del self.info[table_id]['tasks_order'][self.info[table_id]['tasks_order'].index(id)]
            return self.info[table_id]['tasks_info'].pop(id)
        except:
            return 'error'
    
    def rename_table(self, table_id, label):
        if type(table_id) != str:
            table_id = str(table_id)
        try:
            self.info[table_id]['label'] = label
        except:
            return 'error'
    
    def rename_task(self, id, table_id, label):
        if type(table_id) != str:
            table_id = str(table_id)
        if type(id) != str:
            id = str(id)
        try:
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