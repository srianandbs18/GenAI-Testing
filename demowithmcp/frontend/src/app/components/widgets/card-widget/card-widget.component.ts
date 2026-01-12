import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

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
    if (action.data && action.data.action) {
      console.log('Action triggered:', action.data.action);
      // In a real app, this would trigger a new chat message
      alert(`Action: ${action.label}\nWould trigger: ${action.data.action}`);
    } else {
      console.log('Action clicked:', action.label, action.data);
      alert(`Action: ${action.label}`);
    }
  }
}

