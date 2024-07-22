from kfp import dsl
from kfp.components import create_component_from_func, load_component_from_text
from kfp.compiler import Compiler

def add(a: int, b: int) -> int:
    return a + b

# Create a component from the add function
add_op = create_component_from_func(
    add,
    base_image='python:3.8',
    packages_to_install=[]
)

@dsl.pipeline(
    name='Additional Pipeline',
    description='An example pipeline that adds numbers'
)
def additional_pipeline(x: int, y: int):
    task1 = add_op(a=x, b=y)
    task2 = add_op(a=task1.output, b=x)

if __name__ == '__main__':
    Compiler().compile(additional_pipeline, 'test_pipeline.yaml')
