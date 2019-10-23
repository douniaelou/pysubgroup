from timeit import default_timer as timer
from scipy.io import arff
import pandas as pd
import pysubgroup as ps
from pysubgroup.tests.DataSets import get_credit_data



data = get_credit_data()

target = ps.NominalTarget('class', b'bad')
searchSpace = ps.create_nominal_selectors(data, ignore=['class'])
task = ps.SubgroupDiscoveryTask(data, target, searchSpace, result_set_size=10, depth=4, qf=ps.ChiSquaredQF())

print("running DFS")
start = timer()
result = ps.SimpleDFS().execute(task)
end = timer()
print("Time elapsed: ", (end - start))
for (q, sg) in result:
    print(str(q) + ":\t" + str(sg.subgroup_description))