import { Component } from '@angular/core';

@Component({
  selector: 'app-chat-page',
  templateUrl: './chat-page.component.html'
})
export class ChatPageComponent {
  messages: { sender: 'user' | 'assistant'; text: string }[] = [
    { sender: 'assistant', text: 'So your file looks good. Do you need any other help?' }
  ];
  newMessage: string = '';

  sendMessage() {
    if (this.newMessage.trim()) {
      // Add the user's message
      this.messages.unshift({ sender: 'user', text: this.newMessage });

      // Clear the input field
      this.newMessage = '';

      // Simulate an assistant reply
      setTimeout(() => {
        this.messages.unshift({
          sender: 'assistant',
          text: 'Got it! Let me know if there is anything else you need.'
        });
      }, 1000);
    }
  }
}
