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
    'pg_data': TableDefinition(
        name = 'pg_data',
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
    'ch_data': TableDefinition(
        name = 'ch_data',
        column_definitions = {
            'fisc_period': 'LowCardinality(String)',
            'comp_code': 'LowCardinality(String)',
            'account': 'LowCardinality(String)',
            'corr_account': 'LowCardinality(String)',
            'cost_center': 'LowCardinality(String)',
            'order_num': 'LowCardinality(String)',
            'wbs_element': 'LowCardinality(String)',
            'material': 'LowCardinality(String)',
            'trans_type': 'LowCardinality(String)',
            'eval_group': 'LowCardinality(String)',
            'currency': 'LowCardinality(String)',
            'amount': 'Decimal64(3)',
        },
        extra = 'ENGINE = MergeTree()\nORDER BY (fisc_period, comp_code, account)'
    ),
    'os_data': TableDefinition(
        name = 'os_data',
        column_definitions = {
            'fisc_period': {"type": "keyword"},
            'comp_code': {"type": "keyword"},
            'account': {"type": "keyword"},
            'corr_account': {"type": "keyword"},
            'cost_center': {"type": "keyword"},
            'order_num': {"type": "keyword"},
            'wbs_element': {"type": "keyword"},
            'material': {"type": "keyword"},
            'trans_type': {"type": "keyword"},
            'eval_group': {"type": "keyword"},
            'currency': {"type": "keyword"},
            'amount': {"type": "float"},
        }
    ),
    'dd_data': TableDefinition(
        name = 'dd_data',
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
            'amount': 'decimal(17,2)',
        }
    ),
}