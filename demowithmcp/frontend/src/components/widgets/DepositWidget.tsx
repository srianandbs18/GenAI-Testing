import React, { useState } from 'react'
import './DepositWidget.css'

interface DepositWidgetProps {
  data: any
}

function DepositWidget({ data }: DepositWidgetProps) {
  const [formData, setFormData] = useState<any>({})

  if (!data) return <div className="widget-error">No data provided for deposit widget</div>

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('Deposit form submitted:', formData)
    alert(
      `Deposit submitted!\nAmount: ${formData.amount}\nSource: ${formData.source}\nMemo: ${formData.memo || 'N/A'}`
    )
    setFormData({})
  }

  const isFormValid = (): boolean => {
    if (!data?.fields) return false

    const requiredFields = data.fields.filter((f: any) => f.required)
    return requiredFields.every((field: any) => {
      const value = formData[field.name]
      return value !== undefined && value !== null && value !== ''
    })
  }

  const handleFieldChange = (name: string, value: any) => {
    setFormData((prev: any) => ({
      ...prev,
      [name]: value
    }))
  }

  return (
    <div className="deposit-widget">
      <div className="widget-header">
        <h3 className="widget-title">{data.title}</h3>
        {data.description && <p className="widget-description">{data.description}</p>}
      </div>

      <form onSubmit={handleSubmit} className="deposit-form">
        {data.fields?.map((field: any, index: number) => (
          <div key={index} className="form-field">
            <label htmlFor={field.name}>
              {field.label}
              {field.required && <span className="required">*</span>}
            </label>

            {(field.type === 'text' || field.type === 'number' || field.type === 'email') && (
              <input
                id={field.name}
                name={field.name}
                type={field.type}
                placeholder={field.placeholder || ''}
                required={field.required}
                min={field.min}
                max={field.max}
                step={field.step}
                value={formData[field.name] || ''}
                onChange={(e) => handleFieldChange(field.name, e.target.value)}
                className="form-input"
              />
            )}

            {field.type === 'select' && (
              <select
                id={field.name}
                name={field.name}
                required={field.required}
                value={formData[field.name] || ''}
                onChange={(e) => handleFieldChange(field.name, e.target.value)}
                className="form-select"
              >
                <option value="" disabled>
                  Select {field.label}
                </option>
                {field.options?.map((option: any, optIndex: number) => (
                  <option key={optIndex} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            )}

            {field.type === 'textarea' && (
              <textarea
                id={field.name}
                name={field.name}
                placeholder={field.placeholder || ''}
                required={field.required}
                rows={field.rows || 4}
                value={formData[field.name] || ''}
                onChange={(e) => handleFieldChange(field.name, e.target.value)}
                className="form-textarea"
              />
            )}
          </div>
        ))}

        <div className="form-actions">
          <button type="submit" className="submit-button" disabled={!isFormValid()}>
            {data.submitLabel || 'Submit'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default DepositWidget

