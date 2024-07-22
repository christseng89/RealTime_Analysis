from kfp import dsl
from kfp.components import create_component_from_func, OutputPath
from kfp.compiler import Compiler

# Define a simple addition function
def add(a: int, b: int, output_path: OutputPath(int)) -> int:
    result = a + b
    print(f"Adding {a} + {b} = {result}")
    with open(output_path, 'w') as f:
        f.write(str(result))
    return result

# Create a component from the add function
add_op = create_component_from_func(
    add,
    base_image='python:3.8',
    output_component_file='add_component.yaml'  # Save the component definition to a file
)

# Define the pipeline
@dsl.pipeline(
    name='Simple Addition Pipeline',
    description='A simple pipeline that adds two numbers'
)
def addition_pipeline(x: int, y: int):
    add_task = add_op(a=x, b=y)

if __name__ == '__main__':
    # Compile the pipeline
    Compiler().compile(addition_pipeline, 'addition_pipeline.yaml')
