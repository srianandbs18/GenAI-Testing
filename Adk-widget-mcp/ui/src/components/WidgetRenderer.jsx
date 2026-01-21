import React from 'react';
import { ScheduleMeetingWidget } from './ScheduleMeetingWidget';
import { TimezoneSelectorWidget } from './TimezoneSelectorWidget';
import './WidgetRenderer.css';

export function WidgetRenderer({ widget, onAction }) {
  if (!widget) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Connecting to ADK server...</p>
      </div>
    );
  }

  const widgetType = widget.widget_type;

  switch (widgetType) {
    case 'schedule_meeting':
      return <ScheduleMeetingWidget widget={widget} onAction={onAction} />;
    
    case 'timezone_selector':
      return <TimezoneSelectorWidget widget={widget} onAction={onAction} />;
    
    default:
      return (
        <div className="error-container">
          <p>Unknown widget type: {widgetType}</p>
        </div>
      );
  }
}
