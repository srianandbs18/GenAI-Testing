import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-withdrawal-widget',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './withdrawal-widget.component.html',
  styleUrls: ['./withdrawal-widget.component.css']
})
export class WithdrawalWidgetComponent {
  @Input() data: any;
  formData: any = {};

  onSubmit() {
    console.log('Withdrawal form submitted:', this.formData);
    alert(`Withdrawal submitted!\nAmount: ${this.formData.amount}\nDestination: ${this.formData.destination}\nMemo: ${this.formData.memo || 'N/A'}`);
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

