import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {IAnalysisDto} from '../interfaces/analysis-dto';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RestService {
  constructor(private http: HttpClient) {}

    compare(payload: any): Observable<IAnalysisDto> {
      const formData = new FormData();
      formData.append('file1', payload.file1, payload.file1?.name);
      formData.append('file2', payload.file2, payload.file2?.name);
      formData.append('task', payload.task);
      return this.http.post<IAnalysisDto>('http://localhost:8000/compare', formData);
  }
}