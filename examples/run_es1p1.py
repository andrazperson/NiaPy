# encoding=utf8
# This is temporary fix to import module from parent folder
# It will be removed when package is published on PyPI
import sys

sys.path.append("../")
# End of fix

import random
from NiaPy.algorithms.basic import EvolutionStrategy1p1
from NiaPy.task import StoppingTask
from NiaPy.benchmarks import Sphere

# we will run Differential Evolution for 5 independent runs
for i in range(5):
    task = StoppingTask(D=10, nFES=10000, benchmark=Sphere())
    algo = EvolutionStrategy1p1()
    best = algo.run(task)
    print("%s -> %f" % (best[0], best[1]))
