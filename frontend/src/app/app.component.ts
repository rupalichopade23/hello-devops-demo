import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  name = '';
  message = '';
  names: string[] = [];

  constructor(private http: HttpClient) {}

  sayHello() {
    this.http
      .get<{ message: string }>(`/api/hello?name=${encodeURIComponent(this.name)}`)
      .subscribe(res => {
        this.message = res.message;
        this.loadNames();
      });
  }

  loadNames() {
    this.http
      .get<{ names: string[] }>('/api/names')
      .subscribe(res => {
        this.names = res.names;
      });
  }
}