from copper import *

@variable
def benchmark():
    return ['matmul', 'astar']

@task
def build(benchmark):
    print 'Building {}'.format(benchmark)

@task
@depends(build)
def run(benchmark):
    print 'Running {}'.format(benchmark)

main()
