import React from 'react'
import './AccountSummaryWidget.css'

interface AccountSummaryWidgetProps {
  data: any
}

function AccountSummaryWidget({ data }: AccountSummaryWidgetProps) {
  if (!data) return <div className="widget-error">No data provided for account summary widget</div>

  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: data?.currency || 'USD'
    }).format(amount)
  }

  const getTransactionTypeClass = (type: string): string => {
    return type === 'credit' ? 'credit' : 'debit'
  }

  return (
    <div className="account-summary-widget">
      <div className="account-header">
        <h3 className="widget-title">{data.title || 'Account Summary'}</h3>
        <div className="account-number">{data.accountNumber}</div>
        <div className="account-type">{data.accountType}</div>
      </div>

      <div className="balance-section">
        <div className="balance-label">Current Balance</div>
        <div className="balance-amount">{formatCurrency(data.balance)}</div>
        <div className="available-balance">
          Available: {formatCurrency(data.availableBalance || data.balance)}
        </div>
      </div>

      {data.recentTransactions && data.recentTransactions.length > 0 && (
        <div className="transactions-section">
          <h4 className="section-title">Recent Transactions</h4>
          <div className="transactions-list">
            {data.recentTransactions.map((transaction: any, index: number) => (
              <div
                key={index}
                className={`transaction-item ${getTransactionTypeClass(transaction.type)}`}
              >
                <div className="transaction-date">{transaction.date}</div>
                <div className="transaction-description">{transaction.description}</div>
                <div className={`transaction-amount ${transaction.type}`}>
                  {transaction.type === 'credit' ? '+' : '-'}
                  {formatCurrency(Math.abs(transaction.amount))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default AccountSummaryWidget

