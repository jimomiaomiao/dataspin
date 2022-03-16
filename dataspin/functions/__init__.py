
from .function import *


function_class_map = {
    'splitby': SplitByFunction,
    'save': SaveFunction,
    'pk_index': PkIndexFunction,
    'flatten': FlattenFunction,
    'format': FormatFunction,
    'deduplicate': DeduplicateFunction,
    'filter': FilterFunction,
    'merge': MergeFunction
}

def creat_function_with(name: str, args):
    function_class = function_class_map.get(name, Function)
    return function_class(args)