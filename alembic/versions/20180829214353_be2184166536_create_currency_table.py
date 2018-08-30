"""create currency table

Revision ID: be2184166536
Revises:
Create Date: 2018-08-29 21:43:53.034930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be2184166536'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
        op.get_bind().execute(
            """
            CREATE TABLE `currencies` (
                `id` integer NOT NULL,
                `name` varchar(50) DEFAULT NULL,
                `type` varchar(50) DEFAULT NULL,
                `rank` integer(12) DEFAULT NULL,
                `slug` varchar(50) DEFAULT NULL,
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
        )


def downgrade():
    op.drop_table('currencies')
