import logging

from flaskr.utils.env_variables import DATABASE_URL

logger = logging.getLogger(__name__)


def modify_database_url_to_add_dialect() -> str:
    try:
        semi_colon_idx = DATABASE_URL.find(':')
        sql_alchemy_dialect = DATABASE_URL[0:semi_colon_idx] + 'ql+psycopg2'
        new_connection_url = sql_alchemy_dialect + DATABASE_URL[semi_colon_idx::]
        return new_connection_url

    except Exception as e:
        logger.error(e)
        raise
