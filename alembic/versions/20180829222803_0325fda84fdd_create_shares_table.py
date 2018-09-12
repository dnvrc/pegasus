"""create shares table

Revision ID: 0325fda84fdd
Revises: be2184166536
Create Date: 2018-08-29 22:28:03.829074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0325fda84fdd'
down_revision = 'be2184166536'
branch_labels = None
depends_on = None


def upgrade():
        op.get_bind().execute(
            """
            CREATE TABLE `shares` (
                `id` integer NOT NULL AUTO_INCREMENT,
                `currency_id` integer DEFAULT NULL,
                `currency_slug` varchar(50) DEFAULT NULL,
                `marketcap` bigint DEFAULT NULL,
                `price_usd` decimal(25, 6) DEFAULT NULL,
                `sent_in_usd` decimal(25, 6) DEFAULT NULL,
                `sent_by_address` bigint DEFAULT NULL,
                `active_addresses` bigint DEFAULT NULL,
                `block_size` decimal(12, 2) DEFAULT NULL,
                `block_time` decimal(12, 2) DEFAULT NULL,
                `difficulty` decimal(65, 2) DEFAULT NULL,
                `network_hashrate` decimal(65, 2) DEFAULT NULL,
                `transactions` bigint DEFAULT NULL,
                `mining_profitability` decimal(12, 6) DEFAULT NULL,
                `median_transaction_fee` decimal(12, 6) DEFAULT NULL,
                `median_transaction_value` decimal(12, 6) DEFAULT NULL,
                `average_transaction_fee` decimal(12, 6) DEFAULT NULL,
                `average_transaction_value` decimal(12, 6) DEFAULT NULL,
                `social_tweets` integer DEFAULT NULL,
                `date` datetime DEFAULT NULL,
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
        )


def downgrade():
    op.drop_table('shares')
