import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-deposit-widget',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './deposit-widget.component.html',
  styleUrls: ['./deposit-widget.component.css']
})
export class DepositWidgetComponent {
  @Input() data: any;
  formData: any = {};

  onSubmit() {
    console.log('Deposit form submitted:', this.formData);
    alert(`Deposit submitted!\nAmount: ${this.formData.amount}\nSource: ${this.formData.source}\nMemo: ${this.formData.memo || 'N/A'}`);
    // Reset form
    this.formData = {};
  }

  isFormValid(): boolean {
    if (!this.data?.fields) return false;
    
    const requiredFields = this.data.fields.filter((f: any) => f.required);
    return requiredFields.every((field: any) => {
      const value = this.formData[field.name];
      return value !== undefined && value !== null && value !== '';
    });
  }
}

