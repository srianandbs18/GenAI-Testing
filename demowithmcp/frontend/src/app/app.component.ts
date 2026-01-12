import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatbotComponent } from './components/chatbot/chatbot.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, ChatbotComponent],
  template: `
    <div class="app-container">
      <header class="app-header">
        <h1>🏦 Banking Demo with MCP</h1>
        <p>Dynamic UI powered by Google ADK Agent + MCP Server</p>
      </header>
      <main class="app-main">
        <app-chatbot></app-chatbot>
      </main>
    </div>
  `,
  styles: [`
    .app-container {
      max-width: 1200px;
      margin: 0 auto;
    }

    .app-header {
      text-align: center;
      color: white;
      margin-bottom: 30px;
    }

    .app-header h1 {
      font-size: 2.5rem;
      margin-bottom: 10px;
    }

    .app-header p {
      font-size: 1.1rem;
      opacity: 0.9;
    }

    .app-main {
      background: white;
      border-radius: 12px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
      overflow: hidden;
    }
  `]
})
export class AppComponent {
  title = 'Banking Demo with MCP';
}

