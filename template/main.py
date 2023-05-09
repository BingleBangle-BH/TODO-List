from jinja2 import Environment, FileSystemLoader

# Load the template
env = Environment(loader=FileSystemLoader('../docs'))
template = env.get_template('index.html')

# Provide data to fill in the placeholders
data = {
    'title': 'My Website',
    'content': 'Welcome to my website!',
    'author': 'John Smith'
}

# Render the template with the data
output = template.render(data)
print(output)
