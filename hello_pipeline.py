from kfp import dsl
from kfp.components import create_component_from_func
from kfp.compiler import Compiler

def say_hello(name: str) -> str:
    hello_text = f'Hello {name}!'
    print(hello_text)
    return hello_text

# Create a component from the say_hello function
say_hello_op = create_component_from_func(
    say_hello,
    base_image='python:3.8',
    packages_to_install=['kfp==1.8.5']
)

@dsl.pipeline(
    name='Hello Pipeline',
    description='A simple intro pipeline'
)
def hello_pipeline(recipient: str):
    # Create a task from the say_hello_op component
    hello_task = say_hello_op(name=recipient)

if __name__ == '__main__':
    # Compile the pipeline
    Compiler().compile(hello_pipeline, 'hello_pipeline.yaml')
