import React from 'react';
import './ScheduleMeetingWidget.css';

export function ScheduleMeetingWidget({ widget, onAction }) {
  const { properties } = widget;

  const handleDateSelect = (option) => {
    onAction('select_date', {
      date: option.value,
      label: `${option.label} ${option.sublabel}`
    });
  };

  const handleTimeSelect = (option) => {
    onAction('select_time', {
      time: option.value,
      label: option.label
    });
  };

  const handleTimezoneChange = () => {
    onAction('change_timezone');
  };

  const handleAction = (buttonAction) => {
    onAction(buttonAction);
  };

  return (
    <div className="schedule-widget">
      <div className="widget-header">
        <h1>{widget.metadata.title}</h1>
      </div>

      {/* Timezone Display */}
      <div className="timezone-section">
        <div className="timezone-label">{properties.timezone.label}</div>
        <div className="timezone-value">
          {properties.timezone.value}
          {properties.timezone.editable && (
            <button className="timezone-change-btn" onClick={handleTimezoneChange}>
              CHANGE TIME ZONE
            </button>
          )}
        </div>
      </div>

      <div className="divider"></div>

      {/* Date Selector */}
      <div className="date-section">
        <div className="section-label">{properties.date_selector.label}</div>
        <div className="date-buttons">
          {properties.date_selector.options.map((option, index) => (
            <button
              key={index}
              className={`date-button ${option.selected ? 'selected' : ''}`}
              onClick={() => handleDateSelect(option)}
            >
              <div className="date-day">{option.label}</div>
              <div className="date-date">{option.sublabel}</div>
            </button>
          ))}
        </div>
      </div>

      <div className="divider"></div>

      {/* Time Slots */}
      <div className="time-section">
        <div className="section-label">{properties.time_slots.label}</div>
        <div className="time-buttons">
          {properties.time_slots.options.map((option, index) => (
            <button
              key={index}
              className={`time-button ${option.selected ? 'selected' : ''}`}
              onClick={() => handleTimeSelect(option)}
            >
              {option.label}
            </button>
          ))}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="action-buttons">
        {properties.actions.buttons.map((button) => (
          <button
            key={button.id}
            className={`action-button ${button.style} ${!button.enabled ? 'disabled' : ''}`}
            onClick={() => handleAction(button.action)}
            disabled={!button.enabled}
          >
            {button.label}
          </button>
        ))}
      </div>
    </div>
  );
}
