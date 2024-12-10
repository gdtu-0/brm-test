from pandas import Series
from typing import Optional
from ..common import TABLE_DEFINITIONS

def _generate_where_cond(k: str, v: str) -> Optional[str]:
    """Generate where condition"""

    l_eq = []   # EQ - equals
    l_cp = []   # CP - contains pattern
    l_ne = []   # NE - not equals
    l_np = []   # NP - not contains pattern
    cond_str = ''

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
    if l_eq:
        if len(l_eq) == 1:
            cond_str = cond_str + f'{k} = \'{l_eq[0]}\''
        else:
            cond_str = cond_str + f'{k} IN (\'' + '\',\''.join(e for e in l_eq) + '\')'
    if l_cp:
        if l_eq:
            cond_str = cond_str + ' OR '
        if len(l_cp) == 1:
            cond_str = cond_str + f'{k} LIKE \'{l_cp[0]}\''
        else:
            cond_str = cond_str + f'({k} LIKE \'' + f'\' OR {k} LIKE \''.join(e for e in l_cp) + '\')'
    if l_ne:
        if l_eq or l_cp:
            cond_str = cond_str + ' AND '
        if len(l_ne) == 1:
            cond_str = cond_str + f'{k} != \'{l_ne[0]}\''
        else:
            cond_str = cond_str + f'{k} NOT IN (\'' + '\',\''.join(e for e in l_ne) + '\')'
    if l_np:
        if l_eq or l_cp or l_ne:
            cond_str = cond_str + ' AND '
        if len(l_np) == 1:
            cond_str = cond_str + f'{k} NOT LIKE \'{l_np[0]}\''
        else:
            cond_str = cond_str + f'({k} NOT LIKE \'' + f'\' AND {k} NOT LIKE \''.join(e for e in l_np) + '\')'
    # print(f'\nk: {k}\nv: {v}\nl_eq: {l_eq}\nl_cp: {l_cp}\nl_ne: {l_ne}\nl_np: {l_np}\ncond_str: {cond_str}')
    if cond_str != '':
        return cond_str
    else:
        return None

def translate_to_where_cond(mapping_row: Series) -> str:
    """Translate mapping row to SQL where condition"""

    data_fields = TABLE_DEFINITIONS['pg_data'].column_definitions.keys()
    conds = []

    source_prefix = 'src_fld'
    keys_iter = iter(mapping_row.keys())
    for fld_key in keys_iter:
        if str(fld_key).startswith(source_prefix):
            val_key = next(keys_iter)
            field = mapping_row[fld_key]
            condition = ''.join(str(mapping_row[val_key]).split())
            if field in data_fields:
                cond = _generate_where_cond(field, condition)
                if cond:
                    conds.append(f'({cond})')
    out = ''
    if conds:
        out = ' AND '.join(cond for cond in conds)
    return out