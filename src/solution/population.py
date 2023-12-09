#
# 集合
#
from individual import Individual
from constraints import INITIALIZE_INDIVIDUAL_MAX,INDIVISUAL_MAX

class Population:
    _individual_list: []
    def __init__(self,work_num):
        self._individual_list = self._create(work_num)
        

    def _create(self):
        return [Individual(INDIVISUAL_MAX) for _ in range(INITIALIZE_INDIVIDUAL_MAX)]
        