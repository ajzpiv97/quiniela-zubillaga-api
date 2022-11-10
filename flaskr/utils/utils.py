import logging

logger = logging.getLogger(__name__)


def modify_database_url_to_add_dialect(original_str: str) -> str:
    try:
        if original_str is None or original_str == '':
            raise Exception('You need to set DATABASE_URl')
        semi_colon_idx = original_str.find(':')
        sql_alchemy_dialect = original_str[0:semi_colon_idx] + 'ql+psycopg2'
        new_connection_url = sql_alchemy_dialect + original_str[semi_colon_idx::]
        return new_connection_url

    except Exception as e:
        logger.error(e)
        raise
