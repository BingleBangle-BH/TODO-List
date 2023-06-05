from jinja2 import Template, Environment, FileSystemLoader
import logging
class renderpage:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        env = Environment(loader=FileSystemLoader(''))
        self.template = env.get_template('index_template.html')

    def refresh(self):
        pass

    def default(self):
        pass

    def update_page(self, task_details: list, account = "Choose Account"):
        task_list = []
        for element in task_details:
            logging.info(f'Task name: {element[0]}. OwnerID: {element[1][0][0]}. Alias: {element[1][0][1]}')
            name = element[0]
            ownerid = element[1][0][0]
            alias = element[1][0][1]
            print(type(str(name)))
            if alias == 'Alice':
                task_list.append({'name': name, 
                                'ownerid': ownerid, 
                                'alias': alias,
                                'data_filter': '.filter-app'})
            elif alias == 'Bob':
                task_list.append({'name': name, 
                                'ownerid': ownerid, 
                                'alias': alias,
                                'data_filter': '.filter-card'})
            elif alias == 'Charlie':
                task_list.append({'name': name, 
                                'ownerid': ownerid, 
                                'alias': alias,
                                'data_filter': '.filter-web'})


        # task_user = [{'name': 'Alice', 'task': 'clean'}]
        data_filter = ['.filter-app', '.filter-card', '.filter-web']
        output1 = self.template.render(task_user=task_list, account = account)
        with open('../docs/index.html', 'w') as f:
            f.write(output1)
