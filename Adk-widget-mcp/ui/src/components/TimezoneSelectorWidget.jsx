import React from 'react';
import './TimezoneSelectorWidget.css';

export function TimezoneSelectorWidget({ widget, onAction }) {
  const { properties } = widget;
  const [selectedTimezone, setSelectedTimezone] = React.useState(
    properties.timezone_list.options.find(opt => opt.selected)?.value || null
  );

  const handleTimezoneSelect = (option) => {
    setSelectedTimezone(option.value);
  };

  const handleConfirm = () => {
    onAction('confirm_timezone', { timezone: selectedTimezone });
  };

  const handleCancel = () => {
    onAction('cancel_timezone');
  };

  return (
    <div className="timezone-widget">
      <div className="widget-header">
        <h1>{widget.metadata.title}</h1>
      </div>

      <div className="timezone-list-section">
        <div className="section-label">{properties.timezone_list.label}</div>
        <div className="timezone-options">
          {properties.timezone_list.options.map((option, index) => (
            <button
              key={index}
              className={`timezone-option ${selectedTimezone === option.value ? 'selected' : ''}`}
              onClick={() => handleTimezoneSelect(option)}
            >
              <div className="radio-circle">
                {selectedTimezone === option.value && <div className="radio-dot"></div>}
              </div>
              <span>{option.label}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="action-buttons">
        <button className="action-button primary" onClick={handleConfirm}>
          Confirm
        </button>
        <button className="action-button secondary" onClick={handleCancel}>
          Cancel
        </button>
      </div>
    </div>
  );
}
