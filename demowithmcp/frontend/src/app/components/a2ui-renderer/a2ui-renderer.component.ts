import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CardWidgetComponent } from '../widgets/card-widget/card-widget.component';
import { AccountSummaryWidgetComponent } from '../widgets/account-summary-widget/account-summary-widget.component';
import { DepositWidgetComponent } from '../widgets/deposit-widget/deposit-widget.component';
import { WithdrawalWidgetComponent } from '../widgets/withdrawal-widget/withdrawal-widget.component';

@Component({
  selector: 'app-a2ui-renderer',
  standalone: true,
  imports: [
    CommonModule,
    CardWidgetComponent,
    AccountSummaryWidgetComponent,
    DepositWidgetComponent,
    WithdrawalWidgetComponent
  ],
  template: `
    <div class="a2ui-renderer">
      <app-card-widget 
        *ngIf="message?.type === 'card'" 
        [data]="message.data">
      </app-card-widget>
      <app-account-summary-widget 
        *ngIf="message?.type === 'account_summary'" 
        [data]="message.data">
      </app-account-summary-widget>
      <app-deposit-widget 
        *ngIf="message?.type === 'deposit'" 
        [data]="message.data">
      </app-deposit-widget>
      <app-withdrawal-widget 
        *ngIf="message?.type === 'withdrawal'" 
        [data]="message.data">
      </app-withdrawal-widget>
      <div *ngIf="!message || !message.type" class="a2ui-error">
        Invalid A2UI message format
      </div>
      <div *ngIf="message?.type && !isValidType(message.type)" class="a2ui-error">
        Unknown widget type: {{ message.type }}
      </div>
    </div>
  `,
  styles: [`
    .a2ui-renderer {
      width: 100%;
    }

    .a2ui-error {
      padding: 1rem;
      background: #fee;
      color: #c33;
      border-radius: 6px;
      border: 1px solid #fcc;
    }
  `]
})
export class A2UIRendererComponent {
  @Input() message: any;

  isValidType(type: string): boolean {
    return ['card', 'account_summary', 'deposit', 'withdrawal'].includes(type);
  }
}

