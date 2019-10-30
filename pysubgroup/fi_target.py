'''
Created on 29.09.2017

@author: lemmerfn
'''
from collections import namedtuple
from functools import total_ordering
import numpy as np
import pysubgroup as ps



@total_ordering
class FITarget():
    def __repr__(self):
        return "T: Frequent Itemsets"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __lt__(self, other):
        return str(self) < str(other)

    def get_attributes(self):
        return []

    def get_base_statistics(self, data, subgroup, weighting_attribute=None):
        if weighting_attribute is None:
            sg_instances = subgroup.subgroup_description.covers(data)
            return sg_instances.sum()
        else:
            raise NotImplementedError("Attribute weights with numeric targets are not yet implemented.")

    def calculate_statistics(self, subgroup, data, weighting_attribute=None):
        if weighting_attribute is not None:
            raise NotImplementedError("Attribute weights with numeric targets are not yet implemented.")
        sg_instances = subgroup.subgroup_description.covers(data)

        subgroup.statistics['size_sg'] = len(sg_instances)
        subgroup.statistics['size_dataset'] = len(data)


class SimpleCountQF(ps.AbstractInterestingnessMeasure):
    tpl = namedtuple('CountQF_parameters' , ('size'))

    def ensure_statistics(self, subgroup, statistics):
        if (not hasattr(statistics, 'size')):
            if subgroup.statistics:
                statistics = subgroup.statistics
            else:
                statistics = self.calculate_statistics(subgroup, statistics)
        return statistics

    def calculate_constant_statistics(self, task):
        pass

    def calculate_statistics(self, subgroup, data=None):
        if hasattr(subgroup, "representation"):
            cover_arr = subgroup
        else:
            cover_arr = subgroup.covers(data)
        return SimpleCountQF.tpl(np.count_nonzero(cover_arr))


class CountQF(SimpleCountQF, ps.BoundedInterestingnessMeasure):
    def evaluate(self, subgroup, statistics=None):
        statistics = self.ensure_statistics(subgroup, statistics)
        return statistics.size

    def optimistic_estimate(self, subgroup, statistics=None):
        statistics = self.ensure_statistics(subgroup, statistics)
        return statistics.size

    def is_applicable(self, subgroup):
        return isinstance(subgroup.target, FITarget)

    def supports_weights(self):
        return False


class AreaQF(SimpleCountQF):
    def evaluate(self, subgroup, statistics=None):
        statistics = self.ensure_statistics(subgroup, statistics)
        return statistics.size * subgroup.depth

    def is_applicable(self, subgroup):
        return isinstance(subgroup.target, FITarget)

    def supports_weights(self):
        return False
