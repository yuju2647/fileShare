#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'yujun huang'

from utils import database

db_slave = database.db_slave()
db_analysis = database.db_analysis()


def get_real_deposit_users():
    """
    返回mysql 数据库中，首次入金小于60的客户的真实首次入金数据
    返回 list 类型：
        结构：[{
                'ib_account':'.',
               'deposit_currency':'.','
               is_deposit':'..',
               'date_time':'.',
               'deposit_time_1':'',
               'deposit_amount_1':,
               'deposit_time_2':'',
               'deposit_amount_2':,

               }
               ,
               {
                'ib_account':'.',
               'deposit_currency':'.','
               is_deposit':'..',
               'date_time':'.'
               }]
            ，包含字段，
    """
    print "start getting real deposit data"
    sql = '''
            SELECT
                ib_account,
                id,
                first_saving_time,
                is_deposit
            FROM
                USER
            WHERE
                is_deposit < 2700
            AND (type = '' or type is null)
            AND phone IS NOT NULL
            and phone!=''
            and first_saving_time is not null
        '''
    invalid_deposit_users = db_slave.query(sql)
    valid_deposit_users = get_valid_deposit_users(invalid_deposit_users)
    print "done"
    return valid_deposit_users


def get_transactions(user):
    ib_account = user['ib_account']
    time = user['first_saving_time']
    date_time = time[0:4] + time[5:7] + time[8:10]
    sql = '''
            SELECT
                ib_account,
                currency AS deposit_currency,
                amount AS is_deposit,
                date_time
            FROM
                cash_transactions
            WHERE
                ib_account =%s
            AND type = 'Deposits'
            AND date_time>=%s
            ORDER BY
                date_time
        '''
    transactions = db_analysis.query(sql, ib_account, date_time)
    return transactions


def get_valid_deposit_users(invalid_deposit_users):
    def get_each_transactions(invalid_deposit_users):
        def set_id(transaction, user):
            transaction['user_id'] = user['id']

        each_transactions = dict()
        for user in invalid_deposit_users:
            ib_account = user['ib_account']
            each_transactions[ib_account] = get_transactions(user)
            [set_id(transaction, user) for transaction in each_transactions[ib_account]]
        return each_transactions

    def get_valid_transaction(transactions):
        index = 0
        sum_transaction = {"ib_account": None,
                           "user_id":None,
                           "deposit_amount": 0,
                           "deposit_date": None
                           }
        for transaction in transactions:
            if index >= 2:
                break
            is_deposit = transaction['is_deposit']
            deposit_currency = transaction['deposit_currency']
            if deposit_currency != 'USD':
                is_deposit /= 7
            sum_transaction['ib_account'] = transaction['ib_account']
            sum_transaction['user_id'] = transaction['user_id']
            sum_transaction['deposit_amount'] += is_deposit
            sum_transaction['deposit_date'] = transaction['date_time']
            '''
            sum_transaction['deposit_date_{}'.format(index + 1)] = transaction['date_time']
            sum_transaction['deposit_amount_{}'.format(index + 1)] = is_deposit
            '''
            index += 1
            if is_deposit >= 2700:
                break
        if sum_transaction['deposit_amount'] >= 2700:
            return sum_transaction
        else:
            return None

    def pick_first_transactions(each_transactions):
        for ib_account in each_transactions.keys():
            valid_transaction = get_valid_transaction(each_transactions[ib_account])
            if valid_transaction:
                each_transactions[ib_account] = valid_transaction
            else:
                each_transactions.pop(ib_account)

    each_transactions = get_each_transactions(invalid_deposit_users)
    pick_first_transactions(each_transactions)
    return each_transactions.values()


if __name__ == '__main__':
    valid_deposit_users = get_real_deposit_users()
    print 'debug'
