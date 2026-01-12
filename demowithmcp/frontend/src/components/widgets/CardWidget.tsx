import React from 'react'
import './CardWidget.css'

interface CardWidgetProps {
  data: any
}

function CardWidget({ data }: CardWidgetProps) {
  if (!data) return <div className="widget-error">No data provided for card widget</div>

  const handleAction = (action: any) => {
    if (action.data && action.data.action) {
      console.log('Action triggered:', action.data.action)
      alert(`Action: ${action.label}\nWould trigger: ${action.data.action}`)
    } else {
      console.log('Action clicked:', action.label, action.data)
      alert(`Action: ${action.label}`)
    }
  }

  return (
    <div className="card-widget">
      <div className="card-content">
        {data.title && <h3 className="card-title">{data.title}</h3>}
        {data.content && (
          <div className="card-body">
            <p dangerouslySetInnerHTML={{ __html: data.content.replace(/\n/g, '<br>') }} />
          </div>
        )}
        {data.footer && <div className="card-footer">{data.footer}</div>}
      </div>
      {data.actions && data.actions.length > 0 && (
        <div className="card-actions">
          {data.actions.map((action: any, index: number) => (
            <button
              key={index}
              className={`card-action ${action.primary ? 'primary' : ''}`}
              onClick={() => handleAction(action)}
            >
              {action.label}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

export default CardWidget

