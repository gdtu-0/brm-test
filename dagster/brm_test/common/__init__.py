from .mtable import TableDefinition

TABLE_DEFINITIONS = {
    'mapping': TableDefinition(
        name = 'mapping',
        column_definitions = {
            'map_rule_id': 'numeric',
            'map_rule_row': 'numeric',
            'where_cond': 'varchar',
            'src_fld_01': 'varchar',
            'src_val_01': 'varchar',
            'src_fld_02': 'varchar',
            'src_val_02': 'varchar',
            'src_fld_03': 'varchar',
            'src_val_03': 'varchar',
            'src_fld_04': 'varchar',
            'src_val_04': 'varchar',
            'src_fld_05': 'varchar',
            'src_val_05': 'varchar',
            'src_fld_06': 'varchar',
            'src_val_06': 'varchar',
            'src_fld_07': 'varchar',
            'src_val_07': 'varchar',
            'src_fld_08': 'varchar',
            'src_val_08': 'varchar',
            'src_fld_09': 'varchar',
            'src_val_09': 'varchar',
            'src_fld_10': 'varchar',
            'src_val_10': 'varchar',
            'src_fld_11': 'varchar',
            'src_val_11': 'varchar',
            'trg_fld_01': 'varchar',
            'trg_val_01': 'varchar',
            'trg_fld_02': 'varchar',
            'trg_val_02': 'varchar',
            'trg_fld_03': 'varchar',
            'trg_val_03': 'varchar',
            'trg_fld_04': 'varchar',
            'trg_val_04': 'varchar',
            'trg_fld_05': 'varchar',
            'trg_val_05': 'varchar',
            'trg_fld_06': 'varchar',
            'trg_val_06': 'varchar',
            'trg_fld_07': 'varchar',
            'trg_val_07': 'varchar',
            'trg_fld_08': 'varchar',
            'trg_val_08': 'varchar',
            'trg_fld_09': 'varchar',
            'trg_val_09': 'varchar',
            'trg_fld_10': 'varchar',
            'trg_val_10': 'varchar',
            'trg_fld_11': 'varchar',
            'trg_val_11': 'varchar',
        }
    ),
    'data': TableDefinition(
        name = 'data',
        column_definitions = {
            'fisc_period': 'varchar(7)',
            'comp_code': 'varchar(4)',
            'account': 'varchar(10)',
            'corr_account': 'varchar(10)',
            'cost_center': 'varchar(10)',
            'order_num': 'varchar(12)',
            'wbs_element': 'varchar(24)',
            'material': 'varchar(18)',
            'trans_type': 'varchar(3)',
            'eval_group': 'varchar(2)',
            'currency': 'varchar(3)',
            'amount': 'numeric',
        }
    ),
}