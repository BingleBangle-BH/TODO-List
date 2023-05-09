
from substrateinterface import SubstrateInterface, Keypair

from jinja2 import Template, Environment, FileSystemLoader

# Load the template file from the templates directory
env = Environment(loader=FileSystemLoader('../docs'))
template = env.get_template('index.html')

# Define some data to render
data = {
    'name': 'Alice',
    'age': 30,
    'hobbies': ['reading', 'painting', 'hiking'],
}

# Render the template with the data
output = template.render(data=data)

# Print the output to the console
print(output)

# Write the generated HTML to a file
with open('../docs/index.html', 'w') as f:
    f.write(output)

# Create a Substrate interface object to connect to the node
substrate = SubstrateInterface(
    url="http://localhost:9933",
    ss58_format=42, 
    type_registry_preset='substrate-node-template'
)

# Define the account to use for the query
keypair = Keypair.create_from_uri('//Alice')

# Get the latest block hash
block_hash = substrate.get_block_hash()

# Get the block header for the latest block
block_header = substrate.get_block_header(block_hash)

print(f"Latest block header: {block_header}")