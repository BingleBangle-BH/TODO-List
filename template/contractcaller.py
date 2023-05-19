from substrateinterface import SubstrateInterface, Keypair, KeypairType, ContractCode, ContractInstance
import os
import logging
class contractcaller:
    def __init__(self, contract_address: str = None):
        logging.basicConfig(level=logging.INFO)
        self.contract = None
        self.contract_address = contract_address
        self.substrate = SubstrateInterface(
                        url="ws://127.0.0.1:9944",
                        ss58_format=42,
                        type_registry_preset='substrate-node-template')

    def deploy(self) -> str:
        # Default keypair
        keypair = Keypair.create_from_uri('//Alice')

        # Deploy contract
        code = ContractCode.create_from_contract_files(
            metadata_file=os.path.join(os.path.dirname(__file__), '../todo_list/target/ink', 'metadata.json'),
            wasm_file=os.path.join(os.path.dirname(__file__), '../todo_list/target/ink', 'todo_list.wasm'),
            substrate=self.substrate
        )
        self.contract = code.deploy(
            keypair=keypair,
            constructor='default',
            value=0,
            gas_limit={'ref_time': 2599000000, 'proof_size': 119900},
            deployment_salt="",
            upload_code=True,
            storage_deposit_limit=1000000000000
        )
        self.contract_address = self.contract.contract_address
        return self.contract_address

    def connect_contract(self, contract_address: str):
        self.contract = ContractInstance.create_from_address(contract_address=contract_address,
                                                            metadata_file=os.path.join(os.path.dirname(__file__),
                                                                                       '../todo_list/target/ink',
                                                                                       'metadata.json'),
                                                            substrate=self.substrate)

    def read(self, keypair, function: str, args: dict = {}) -> dict:
        result = self.contract.read(keypair, function, args)
        # return result.contract_result_data
        return result

    def exec(self, keypair, function: str, args: dict, gas_limit):
        contract_receipt = self.contract.exec(keypair, function, args=args, gas_limit=gas_limit)
        return contract_receipt
    
    def check_balance(self, address):
        result = self.substrate.query('System', 'Account', [address])
        return result
    
    def transfer(self, from_keypair, dest_keypair):
        call = self.substrate.compose_call(call_module='Balances',
                                            call_function='transfer',
                                            call_params={
                                                'dest': dest_keypair.ss58_address,
                                                'value': 1 * 10**10
                                            })
 
        extrinsic = self.substrate.create_signed_extrinsic(call=call, keypair=from_keypair)
        receipt = self.substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        return receipt

