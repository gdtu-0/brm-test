from pandas import Series
from ..common import TABLE_DEFINITIONS

def _generate_where_cond(k: str, v: str) -> str:
    """Generate where condition"""

    l_eq = []   # EQ - equals
    l_cp = []   # CP - contains pattern
    l_ne = []   # NE - not equals
    l_np = []   # NP - not contains pattern

    for element in v.split(','):
        if '*' in element or '+' in element:
            element = element.replace('*', '%')
            element = element.replace('+', '_')
            if element.startswith('~'):
                l_np.append(element[1:])
            else:
                if element == '%':
                    continue
                l_cp.append(element)
        else:
            if element.startswith('~'):
                l_ne.append(element[1:])
            else:
                if element == '#':
                    element = ''
                l_eq.append(element)
    print(f'l_eq: {l_eq}\nl_cp: {l_cp}\nl_ne: {l_ne}\nl_np: {l_np}')

def translate_to_where_cond(mapping_row: Series) -> str:
    """Translate mapping row to SQL where condition"""

    data_fields = TABLE_DEFINITIONS['data'].column_definitions.keys()

    source_prefix = 'src_fld'
    keys_iter = iter(mapping_row.keys())
    for fld_key in keys_iter:
        if str(fld_key).startswith(source_prefix):
            val_key = next(keys_iter)
            field = mapping_row[fld_key]
            condition = ''.join(str(mapping_row[val_key]).split())
            if field in data_fields:
                print(f'\nk: {field}\nv: {condition}')
                _generate_where_cond(field, condition)