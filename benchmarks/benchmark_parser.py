import timeit

setup_code = '''
import json
with open('examples/complex.stj.json', 'r', encoding='utf-8') as f:
    data = f.read()
'''

test_code = '''
json.loads(data)
'''

execution_time = timeit.timeit(stmt=test_code, setup=setup_code, number=1000)
print(f"Average parsing time: {execution_time / 1000:.6f} seconds per run")
