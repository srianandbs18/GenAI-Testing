import { Component, OnInit, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { A2UIRendererComponent } from '../a2ui-renderer/a2ui-renderer.component';

interface Message {
  id: number;
  type: 'user' | 'bot';
  text?: string;
  a2ui?: any;
  timestamp: Date;
}

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule, A2UIRendererComponent],
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent implements OnInit, AfterViewChecked {
  messages: Message[] = [
    {
      id: 1,
      type: 'bot',
      text: 'Hello! I can demonstrate A2UI widgets. Try these commands:\n\n• "show card" or "display card" - Display a card widget\n• "show form" or "display form" - Display a form widget\n• "show table" or "display table" - Display a data table widget\n• "show all" - Display all widgets',
      timestamp: new Date()
    }
  ];
  inputText: string = '';
  isLoading: boolean = false;
  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    console.log('Chatbot component initialized');
  }

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  scrollToBottom(): void {
    try {
      if (this.messagesContainer) {
        this.messagesContainer.nativeElement.scrollTop = 
          this.messagesContainer.nativeElement.scrollHeight;
      }
    } catch (err) {
      console.error('Error scrolling:', err);
    }
  }

  async handleSend() {
    if (!this.inputText.trim() || this.isLoading) return;

    const userMessage: Message = {
      id: Date.now(),
      type: 'user',
      text: this.inputText.trim(),
      timestamp: new Date()
    };

    this.messages.push(userMessage);
    const prompt = this.inputText.trim();
    this.inputText = '';
    this.isLoading = true;

    try {
      // Send prompt to ADK agent
      const response = await this.http.post<any>(
        'http://localhost:8001/chat',
        { message: prompt }
      ).toPromise();

      const botMessage: Message = {
        id: Date.now() + 1,
        type: 'bot',
        text: response.text || 'Here is the widget:',
        a2ui: response.a2ui,
        timestamp: new Date()
      };

      this.messages.push(botMessage);
    } catch (error) {
      console.error('Error communicating with agent:', error);
      const errorMessage: Message = {
        id: Date.now() + 1,
        type: 'bot',
        text: 'Sorry, I encountered an error. Please make sure the ADK agent is running on http://localhost:8001',
        timestamp: new Date()
      };
      this.messages.push(errorMessage);
    } finally {
      this.isLoading = false;
    }
  }

  onKeyPress(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.handleSend();
    }
  }
}

