import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {MainPageComponent} from './views/main-page/main-page.component';
import {ChatPageComponent} from './views/chat-page/chat-page.component';

const routes: Routes = [
  { path: '', component: MainPageComponent },
  { path: 'chat', component: ChatPageComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
