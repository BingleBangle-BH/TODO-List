
from jinja2 import Template, Environment, FileSystemLoader
import logging
from dotenv import load_dotenv, find_dotenv
from substrateinterface import SubstrateInterface, Keypair, KeypairType, ContractCode, ContractInstance
from render import renderpage
from contractcaller import contractcaller
import os

# substrate = SubstrateInterface(
#     url="ws://127.0.0.1:9944",
#     ss58_format=42,
#     type_registry_preset='substrate-node-template',
# )

# keypair = Keypair.create_from_uri('//Bob')
# contract = contractcaller()
# contract.deploy()

# # Deploy contract
# code = ContractCode.create_from_contract_files(
#     metadata_file=os.path.join(os.path.dirname(__file__), '../todo_list/target/ink', 'metadata.json'),
#     wasm_file=os.path.join(os.path.dirname(__file__), '../todo_list/target/ink', 'todo_list.wasm'),
#     substrate=substrate
# )

# contract_address = '5DJx3dr54EJP2uWm3E8WctWMnjXk94v6r1gxY9us4bTZdQVd'
# contract = contractcaller(contract_address=contract_address)
# contract.connect_contract()
# result = contract.read(keypair=keypair,
#                        function='create_task',
#                        args={'init_alias': 'Alice','init_task': 'clean the table'})

# print('Executing contract call...')
# contract_receipt = contract.exec(keypair, 
#                                  'create_task', 
#                                  args={'init_alias': 'Alice','init_task': 'clean the table'}, 
#                                  gas_limit=result.gas_required)

# print(contract_receipt)

# result = contract.read(keypair=keypair,
#                        function='get_all',
#                        args={'_task': 'clean the table'})

# print(result.contract_result_data)

class logic:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.contract_address = None
        self.aliaslist = ['Alice', 'Bob', 'Charlie']
        self.keypairlist = [Keypair.create_from_uri('//Alice'), 
                    Keypair.create_from_uri('//Bob'),
                    Keypair.create_from_uri('//Charlie')]
        pass

    def setup(self):
        tasklist = ['Wash the plates', 'Clean the cabinets', 'Wipe the table', 
                    'Pack the storeroom', 'Iron the clothes', 'Unload the weights',
                    'Feed the pets', 'Buy kibbles', 'Nap with cat']

        contract = contractcaller()
        self.contract_address = contract.deploy() # Deploy contract
        logging.info(f'✅ Deployed @ {self.contract_address}')
        with open(".env", "w") as f:
            f.write(f'contract_address={self.contract_address}')
    
        for key in self.keypairlist:
            result = contract.check_balance(key.ss58_address)
            balance = result.value['data']['free']
            if balance < 1 * 10**5:
                receipt = contract.transfer(self.keypairlist[0], key)
                logging.info(f'Extrinsic "{receipt.extrinsic_hash}" sent and included in block "{receipt.block_hash}"')

        for i in range(0,4):
            contract.connect_contract(self.contract_address)
            keypair = self.keypairlist[i%3]
            alias = self.aliaslist[i%3]
            task = tasklist[i]
            result = contract.read(keypair=keypair,
                                    function='create_task',
                                    args={'init_alias': alias,'init_task': task})

            contract_receipt = contract.exec(keypair=keypair, 
                                        function='create_task', 
                                        args={'init_alias': alias,'init_task': task}, 
                                        gas_limit=result.gas_required)
            
            logging.info(f'Task {i+1} result : {contract_receipt.is_success}')

        result = contract.read(keypair=self.keypairlist[0],
                               function='get_all_task')
        # logging.info(f'Result : {result.contract_result_data}')
        for index, element in enumerate(result.contract_result_data):
            if index == 1:
                logging.info(f'Result : {element}')
                page = renderpage()
                page.update_page(element)
                break

    def update_account(self, alias):
        self.contract_address = os.getenv('contract_address')
        contract = contractcaller(self.contract_address)
        result = contract.read(keypair=self.keypairlist[0],
                               function='get_all_task')
        for index, element in enumerate(result.contract_result_data):
            if index == 1:
                logging.info(f'Result : {element}')
                page = renderpage()
                page.update_page(element, alias)
                break


    def connect(self):
        pass

    def create_account(self):
        pass

    def create_task(self):
        pass

    def modify_task(self, new_task = str, old_task = str):
        contract = contractcaller(self.contract_address)
        contract.connect_contract(self.contract_address)
        # result = contract.read(keypair=keypair,
        #                             function='create_task',
        #                             args={'init_alias': alias,'init_task': task})

        pass

    def remove_task(self):
        pass

    def get_task(self):
        pass   


if __name__ == "__main__":
    exec = logic()
    exec.setup()
    load_dotenv(find_dotenv())


# renderobj = renderpage()
# renderobj.update(task = result)


# contract = code.deploy(
#     keypair=keypair,
#     constructor='new',
#     args={'init_task': 'Wash toilet', 'init_alias': 'Alice'},
#     value=0,
#     gas_limit={'ref_time': 2599000000, 'proof_size': 119900},
#     deployment_salt="",
#     upload_code=True,
#     storage_deposit_limit=1000000000000
# )

# print(f'✅ Deployed @ {contract.contract_address}')

# Create contract instance from deterministic address
# contract = ContractInstance.create_from_address(
#     contract_address=contract_address,
#     metadata_file=os.path.join(os.path.dirname(__file__), '../todo_list/target/ink', 'metadata.json'),
#     substrate=substrate
# )
# result = contract.read(keypair, 'get_task')
# print(result.contract_result_data)

# Do a gas estimation of the message
# gas_predit_result = contract.read(keypair, 
#                                   'modify_task',
#                                   args={'new_task': 'clean the table'})

# print('Result of dry-run: ', gas_predit_result.value)
# print('Gas estimate: ', gas_predit_result.gas_required)

# Do the actual call
# print('Executing contract call...')
# contract_receipt = contract.exec(keypair, 
#                                  'modify_task', 
#                                  args={'new_task': 'clean the table'}, 
#                                  gas_limit=gas_predit_result.gas_required)



# if contract_receipt.is_success:
#     print(f'Events triggered in contract: {contract_receipt.contract_events}')
# else:
#     print(f'Error message: {contract_receipt.error_message}')

# # Create a Substrate interface object to connect to the node
# substrate = SubstrateInterface(
#     url="http://localhost:9933",
# )

# # Define the account to use for the query
# keypair = Keypair.create_from_uri('//Alice')

# # Get the latest block hash
# block_hash = substrate.get_block_hash()

# # Get the block header for the latest block
# block_header = substrate.get_block_header(block_hash)

# print(f"Latest block header: {block_header}")

# # Load the template file from the templates directory
# env = Environment(loader=FileSystemLoader('../docs'))
# template = env.get_template('index.html')

# # Define some data to render
# data = {
#     'name': 'Alice',
#     'age': 30,
#     'hobbies': ['reading', 'painting', 'hiking'],
# }

# # Render the template with the data
# output = template.render(data=data)

# # Print the output to the console
# print(output)

# # Write the generated HTML to a file
# with open('../docs/index.html', 'w') as f:
#     f.write(output)