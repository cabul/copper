from copper import Copper, depends, nocache

app = Copper('run experiments')

@app.variable
def benchmark():
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

@app.variable
@depends(run)
def metric(benchmark):
    if benchmark == 'matmul':
        return ['ipc', 'mpki']
    else:
        return ['branches']

@app.task
def plot(benchmark, metric):
    print 'Plotting {} for {}'.format(metric, benchmark)

app.main()
