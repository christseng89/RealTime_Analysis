from kfp import dsl
from kfp.compiler import Compiler
from kfp.components import load_component_from_text

# Define the component using YAML
add_op_yaml = '''
name: Add
description: Adds two integers
inputs:
  - {name: a, type: Integer}
  - {name: b, type: Integer}
outputs:
  - {name: output, type: Integer}
implementation:
  container:
    image: python:3.8
    command:
    - python3
    - -c
    - |
      import argparse
      import os

      def add(a, b):
          result = a + b
          print(f"Adding {a} + {b} = {result}")
          with open("/tmp/output", "w") as f:
              f.write(str(result))

      if __name__ == "__main__":
          _parser = argparse.ArgumentParser(prog='Add', description='')
          _parser.add_argument("--a", dest="a", type=int, required=True)
          _parser.add_argument("--b", dest="b", type=int, required=True)
          _parser.add_argument("----output-paths", dest="_output_paths", type=str, nargs=1)
          _parsed_args = vars(_parser.parse_args())
          _output_files = _parsed_args.pop("_output_paths", [])

          _outputs = add(**_parsed_args)

          with open(_output_files[0], 'w') as f:
              f.write(str(_outputs))
    fileOutputs:
      output: /tmp/output
'''

add_op = load_component_from_text(add_op_yaml)

@dsl.pipeline(
    name='Simple Addition Pipeline',
    description='A simple pipeline that adds two numbers'
)
def addition_pipeline(x: int, y: int):
    add_task = add_op(a=x, b=y)

if __name__ == '__main__':
    Compiler().compile(addition_pipeline, 'addition_pipeline.yaml')
