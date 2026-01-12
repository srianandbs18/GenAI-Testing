import React from 'react'
import CardWidget from './widgets/CardWidget'
import AccountSummaryWidget from './widgets/AccountSummaryWidget'
import DepositWidget from './widgets/DepositWidget'
import WithdrawalWidget from './widgets/WithdrawalWidget'
import './A2UIRenderer.css'

interface A2UIRendererProps {
  message: any
}

function A2UIRenderer({ message }: A2UIRendererProps) {
  if (!message || !message.type) {
    return <div className="a2ui-error">Invalid A2UI message format</div>
  }

  const validTypes = ['card', 'account_summary', 'deposit', 'withdrawal']
  if (!validTypes.includes(message.type)) {
    return <div className="a2ui-error">Unknown widget type: {message.type}</div>
  }

  return (
    <div className="a2ui-renderer">
      {message.type === 'card' && <CardWidget data={message.data} />}
      {message.type === 'account_summary' && <AccountSummaryWidget data={message.data} />}
      {message.type === 'deposit' && <DepositWidget data={message.data} />}
      {message.type === 'withdrawal' && <WithdrawalWidget data={message.data} />}
    </div>
  )
}

export default A2UIRenderer

