import {Component, OnInit} from '@angular/core';
import {RestService} from '../../services/rest.service';

@Component({
  selector: 'app-chat-page',
  templateUrl: './chat-page.component.html'
})
export class ChatPageComponent implements OnInit{

  newMessage: string = '';
  firstMessage: string = '';

  constructor(public restService: RestService) {}

  ngOnInit(): void {
    // Get the data from the main page
    const data = history.state.data;
    const message = data.analysis;
    this.firstMessage = message;
  }

  messages: { sender: 'user' | 'assistant'; text: string }[] = [
    { sender: 'assistant', text: 'Do you have any questions?' },
  ];

  sendMessage() {
    if (this.newMessage.trim()) {
      // Add the user's message
      this.messages.unshift({ sender: 'user', text: this.newMessage });

      // Send the user's message to the server
      this.restService.compare({task: this.newMessage},true).subscribe((response) => {
        // Add the assistant's response
        this.messages.unshift({ sender: 'assistant', text: response.analysis });
      });
      // Clear the input field
      this.newMessage = '';
    }
  }


}
