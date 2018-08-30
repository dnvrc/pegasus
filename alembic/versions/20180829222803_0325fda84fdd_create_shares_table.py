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
                `id` integer NOT NULL,
                `currency_id` integer NOT NULL,
                `currency_slug` varchar(50) DEFAULT NULL,
                `transactions` varchar(75) DEFAULT NULL,
                `block_size` varchar(75) DEFAULT NULL,
                `block_time` varchar(75) DEFAULT NULL,
                `difficulty` varchar(75) DEFAULT NULL,
                `network_hashrate` varchar(75) DEFAULT NULL,
                `price_usd` varchar(75) DEFAULT NULL,
                `price_btc` varchar(75) DEFAULT NULL,
                `sent_in_usd` varchar(75) DEFAULT NULL,
                `sent_by_address` varchar(75) DEFAULT NULL,
                `marketcap` varchar(75) DEFAULT NULL,
                `mining_profitability` varchar(75) DEFAULT NULL,
                `median_transaction_fee` varchar(75) DEFAULT NULL,
                `median_transaction_value` varchar(75) DEFAULT NULL,
                `average_transaction_fee` varchar(75) DEFAULT NULL,
                `average_transaction_value` varchar(75) DEFAULT NULL,
                `social_tweets` varchar(75) DEFAULT NULL,
                `active_addresses` varchar(75) DEFAULT NULL,
                `date` datetime DEFAULT NULL,
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
        )


def downgrade():
    op.drop_table('shares')
