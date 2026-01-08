import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

/**
 * Card Widget Template
 * Displays information in a card format with title, content, and optional actions
 */
@Component({
  selector: 'app-card-widget',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './card-widget.component.html',
  styleUrls: ['./card-widget.component.css']
})
export class CardWidgetComponent {
  @Input() data: any;

  handleAction(action: any) {
    if (action.onClick) {
      action.onClick();
    } else {
      console.log('Action clicked:', action.label, action.data);
      alert(`Action: ${action.label}\nData: ${JSON.stringify(action.data || {}, null, 2)}`);
    }
  }
}

