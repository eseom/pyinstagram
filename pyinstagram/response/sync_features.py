from pyinstagram.module.printable import Printable


class Param(Printable):
    def __init__(self, dict_data):
        self.name = dict_data['name']
        self.value = dict_data['value']


class Experiment(Printable):
    def __init__(self, data):
        self.params = [Param(param) for param in data['params']]
        self.group = data['group']
        self.name = data['name']


class SyncFeaturesResponse(Printable):
    def __init__(self, experiments):
        self.experiments = [Experiment(experiment) for experiment in
                            experiments]

