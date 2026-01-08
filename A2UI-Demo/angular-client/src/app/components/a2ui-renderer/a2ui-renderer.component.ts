import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CardWidgetComponent } from '../widgets/card-widget/card-widget.component';
import { FormWidgetComponent } from '../widgets/form-widget/form-widget.component';
import { DataTableWidgetComponent } from '../widgets/data-table-widget/data-table-widget.component';

/**
 * A2UI Message Renderer
 * Parses A2UI protocol messages and renders the appropriate widget
 */
@Component({
  selector: 'app-a2ui-renderer',
  standalone: true,
  imports: [
    CommonModule,
    CardWidgetComponent,
    FormWidgetComponent,
    DataTableWidgetComponent
  ],
  template: `
    <div class="a2ui-renderer">
      <app-card-widget *ngIf="message?.type === 'card'" [data]="message.data"></app-card-widget>
      <app-form-widget *ngIf="message?.type === 'form'" [data]="message.data"></app-form-widget>
      <app-data-table-widget *ngIf="message?.type === 'table' || message?.type === 'datatable'" [data]="message.data"></app-data-table-widget>
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
    return ['card', 'form', 'table', 'datatable'].includes(type);
  }
}

