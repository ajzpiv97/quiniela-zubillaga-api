def modify_database_url_to_add_dialect(original_str: str) -> str:
    semi_colon_idx = original_str.find(':')
    sql_alchemy_dialect = original_str[0:semi_colon_idx] + 'ql+psycopg2'
    new_connection_url = sql_alchemy_dialect + original_str[semi_colon_idx::]
    return new_connection_url
