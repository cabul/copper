'''simple copper example'''

from copper import *

@variable
def benchmark():
    '''list of benchmarks to run'''
    return ['matmul', 'astar']

@task
def build(benchmark):
    '''build/compile a benchmark'''
    print 'Building {}'.format(benchmark)

# @task
# @depends(build)
# def run(benchmark):
#     print 'Running {}'.format(benchmark)

main(__doc__)
