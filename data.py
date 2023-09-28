import json

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
