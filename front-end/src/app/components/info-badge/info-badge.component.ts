import { Component } from '@angular/core';

@Component({
  selector: 'app-info-badge',
  templateUrl: './info-badge.component.html'
})
export class InfoBadgeComponent {
  isPopupVisible: boolean = false;

  togglePopup(): void {
    this.isPopupVisible = !this.isPopupVisible;
    document.body.style.overflow = this.isPopupVisible ? 'hidden' : '';
  }

  closePopup(event: MouseEvent): void {
    const target = event.target as HTMLElement;
    if (target.classList.contains('popup-overlay')) {
      this.isPopupVisible = false;
      document.body.style.overflow = '';
    }
  }
}
