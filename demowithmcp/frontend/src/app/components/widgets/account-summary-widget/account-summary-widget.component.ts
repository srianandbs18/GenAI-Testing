import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-account-summary-widget',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './account-summary-widget.component.html',
  styleUrls: ['./account-summary-widget.component.css']
})
export class AccountSummaryWidgetComponent {
  @Input() data: any;

  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: this.data?.currency || 'USD'
    }).format(amount);
  }

  getTransactionTypeClass(type: string): string {
    return type === 'credit' ? 'credit' : 'debit';
  }
}

