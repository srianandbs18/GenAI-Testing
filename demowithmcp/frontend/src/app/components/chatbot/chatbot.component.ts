import { Component, OnInit, AfterViewChecked, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { A2UIRendererComponent } from '../a2ui-renderer/a2ui-renderer.component';

interface Message {
  id: number;
  type: 'user' | 'bot';
  text: string;
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
  @ViewChild('messagesContainer') messagesContainer!: ElementRef;

  messages: Message[] = [];
  inputText: string = '';
  isLoading: boolean = false;
  private readonly agentUrl = 'http://localhost:8001';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    // Welcome message
    this.messages.push({
      id: 0,
      type: 'bot',
      text: 'Hello! I\'m your banking assistant. I can help you with:\n\n• View account summary\n• Make deposits\n• Process withdrawals\n\nWhat would you like to do?',
      timestamp: new Date()
    });
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
      const response = await this.http.post<any>(
        `${this.agentUrl}/chat`,
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
    } catch (error: any) {
      console.error('Error communicating with agent:', error);
      const errorMessage: Message = {
        id: Date.now() + 1,
        type: 'bot',
        text: `Sorry, I encountered an error. ${error.message || 'Please make sure the agent is running on http://localhost:8001'}`,
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

