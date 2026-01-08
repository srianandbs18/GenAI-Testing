import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatbotComponent } from './components/chatbot/chatbot.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, ChatbotComponent],
  template: `
    <div class="app">
      <header class="app-header">
        <h1>A2UI Demo - Chatbot with Widget Templates</h1>
        <p>Interactive chatbot demonstrating A2UI protocol with 3 widget templates</p>
        <p class="subtitle">Powered by Google ADK Agent + Angular</p>
      </header>
      <main class="app-main">
        <app-chatbot></app-chatbot>
      </main>
    </div>
  `,
  styles: [`
    .app {
      display: flex;
      flex-direction: column;
      height: 100vh;
      width: 100%;
    }

    .app-header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 1.5rem 2rem;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .app-header h1 {
      font-size: 1.75rem;
      margin-bottom: 0.5rem;
    }

    .app-header p {
      font-size: 0.95rem;
      opacity: 0.9;
    }

    .subtitle {
      font-size: 0.85rem !important;
      opacity: 0.8 !important;
      margin-top: 0.25rem;
    }

    .app-main {
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 2rem;
      overflow: hidden;
    }
  `]
})
export class AppComponent implements OnInit {
  ngOnInit() {
    console.log('A2UI Demo App initialized');
  }
}

