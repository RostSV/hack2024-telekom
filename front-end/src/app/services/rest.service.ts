import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RestService {

  constructor(private http: HttpClient) {}
  compare(payload: any, isDraft: boolean): Observable<any> {
    const formData = new FormData();
    const emptyBlob = new Blob();
    if(!isDraft) {
      formData.append('file1', payload.file1, payload.file1?.name);
      formData.append('file2', payload.file2, payload.file2?.name);
      formData.append('task', payload.task);
    }else{
      formData.append('file1',emptyBlob);
      formData.append('file2',emptyBlob);
      formData.append('task', payload.task);
    }

    return this.http.post<any>('http://localhost:8000/compare', formData);
  }
}
