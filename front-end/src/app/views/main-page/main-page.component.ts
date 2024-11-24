import { Component } from '@angular/core';
import {RestService} from '../../services/rest.service';

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html'
})
export class MainPageComponent {
  file1: File | null = null;
  file2: File | null = null;
  steps = 0;
  instructions = "";
  shouldAnimate = false;
  isLoading: boolean;

  constructor(private service: RestService) {
    this.isLoading = false;
  }

  triggerFileInput(steps: any): void {
    const fileInput = document.getElementById('fileInput') as HTMLInputElement;
    const fileInput2 = document.getElementById('fileInput2') as HTMLInputElement;
    if (fileInput && steps === 1) {
      fileInput.click();
    } else if (fileInput2) {
      fileInput2.click();
    }
    this.shouldAnimate = false;
  }

  onFileSelected1(event: Event): void {
    const input: HTMLInputElement = event.target as HTMLInputElement;
    if (!input.files) return;
    this.file1 = input?.files[0];
    this.steps++;
    this.shouldAnimate = true;
  }

  onFileSelected2(event: Event): void {
    const input: HTMLInputElement = event.target as HTMLInputElement;
    if (!input.files) return;
    this.file2 = input?.files[0];
    this.steps++;
    this.shouldAnimate = true;
  }

  onButtonClick() {
    this.steps++;

    const payload = {
      task: this.instructions ? this.instructions : 'validate',
      file1: this.file1,
      file2: this.file2
    }
    this.isLoading = true;
    this.service.compare(payload).subscribe(
      (response) => {
        this.isLoading = false;
      },
      (error) => {
        console.error('Comparison failed:', error);
        this.isLoading = false;
      }
    );
  }

  getIcon(name: string | undefined) {
    name = name ? name : '';
    const extension = name.substring(name.lastIndexOf('.'));
    switch (extension) {
      case '.pdf':
        return 'fa-regular fa-file-pdf';
      default:
        return 'fa-regular fa-file';
    }
  }
}
