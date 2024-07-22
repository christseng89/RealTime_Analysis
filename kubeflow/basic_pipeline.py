from kfp import dsl
from kfp.components import create_component_from_func
from kfp.compiler import Compiler

# Define a simple function
def print_message(message: str):
    print(message)

# Create a component from the function
print_message_op = create_component_from_func(print_message, base_image='python:3.8')

@dsl.pipeline(
    name='Basic Pipeline',
    description='A basic pipeline that prints a message'
)
def basic_pipeline(message: str):
    print_task = print_message_op(message=message)

if __name__ == '__main__':
    Compiler().compile(basic_pipeline, 'basic_pipeline.yaml')
