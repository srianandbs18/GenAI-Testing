import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

/**
 * Form Widget Template
 * Displays an interactive form with various input types
 */
@Component({
  selector: 'app-form-widget',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './form-widget.component.html',
  styleUrls: ['./form-widget.component.css']
})
export class FormWidgetComponent {
  @Input() data: any;
  formData: any = {};
  errors: any = {};

  handleChange(fieldName: string, value: any) {
    this.formData[fieldName] = value;
    if (this.errors[fieldName]) {
      delete this.errors[fieldName];
    }
  }

  validateField(field: any, value: any): string | null {
    if (field.required && !value) {
      return `${field.label} is required`;
    }
    if (field.type === 'email' && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      return 'Please enter a valid email address';
    }
    return null;
  }

  handleSubmit() {
    if (!this.data || !this.data.fields) return;

    const newErrors: any = {};
    
    this.data.fields.forEach((field: any) => {
      const value = this.formData[field.name];
      const error = this.validateField(field, value);
      if (error) {
        newErrors[field.name] = error;
      }
    });

    if (Object.keys(newErrors).length > 0) {
      this.errors = newErrors;
      return;
    }

    console.log('Form submitted:', this.formData);
    alert(`Form submitted successfully!\n\nData: ${JSON.stringify(this.formData, null, 2)}`);
    
    if (this.data.onSubmit) {
      this.data.onSubmit(this.formData);
    }
  }

  formatCellValue(value: any): string {
    if (value === null || value === undefined) return '-';
    if (typeof value === 'boolean') return value ? '✓' : '✗';
    if (typeof value === 'object') return JSON.stringify(value);
    return value;
  }
}

