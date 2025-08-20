# (C) 2021 GoodData Corporation


def _tables_to_dict(tables):
    return dict([(t.table_name, t) for t in tables])
