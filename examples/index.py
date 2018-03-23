from copper import Copper, depends, nocache

app = Copper('run experiments')

@app.variable
def benchmark():
    '''list of benchmarks to run'''
    return ['matmul', 'astar']

@app.task
def build(benchmark):
    '''build/compile a benchmark'''
    print 'Building {}'.format(benchmark)

@app.task
@depends(build)
@nocache
def run(benchmark):
    '''run a benchmark'''
    print 'Running {}'.format(benchmark)

app.main()
