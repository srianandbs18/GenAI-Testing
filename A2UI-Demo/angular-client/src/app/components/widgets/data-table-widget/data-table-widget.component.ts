import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

/**
 * Data Table Widget Template
 * Displays data in a table format with sorting and optional actions
 */
@Component({
  selector: 'app-data-table-widget',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './data-table-widget.component.html',
  styleUrls: ['./data-table-widget.component.css']
})
export class DataTableWidgetComponent {
  @Input() data: any;
  sortConfig: { key: string | null; direction: 'asc' | 'desc' } = { key: null, direction: 'asc' };

  handleSort(key: string) {
    let direction: 'asc' | 'desc' = 'asc';
    if (this.sortConfig.key === key && this.sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    this.sortConfig = { key, direction };
  }

  getSortedRows(): any[] {
    if (!this.data || !this.data.rows) return [];
    if (!this.sortConfig.key) return this.data.rows;

    return [...this.data.rows].sort((a, b) => {
      const aValue = a[this.sortConfig.key!];
      const bValue = b[this.sortConfig.key!];

      if (aValue === null || aValue === undefined) return 1;
      if (bValue === null || bValue === undefined) return -1;

      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return this.sortConfig.direction === 'asc' ? aValue - bValue : bValue - aValue;
      }

      const aStr = String(aValue).toLowerCase();
      const bStr = String(bValue).toLowerCase();

      if (this.sortConfig.direction === 'asc') {
        return aStr.localeCompare(bStr);
      } else {
        return bStr.localeCompare(aStr);
      }
    });
  }

  formatCellValue(value: any): string {
    if (value === null || value === undefined) return '-';
    if (typeof value === 'boolean') return value ? '✓' : '✗';
    if (typeof value === 'object') return JSON.stringify(value);
    return value;
  }

  handleAction(action: any, row: any, rowIndex: number) {
    if (action.onClick) {
      action.onClick(row, rowIndex);
    } else {
      console.log('Action clicked:', action.label, row);
      alert(`Action: ${action.label}\nRow: ${JSON.stringify(row, null, 2)}`);
    }
  }
}

