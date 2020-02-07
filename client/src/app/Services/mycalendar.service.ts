import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {DatePipe} from '@angular/common'
import {Event} from '../Models/event';
import { User } from '../Models/user';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class MyCalendarService {
    private BASE_URL: string = 'http://localhost:5000/api/mycalendar/events';
    private BASE_URL2: string = 'http://localhost:5000/api/listtest';
    private headers: HttpHeaders = new HttpHeaders({'Content-Type': 'application/json'});
    
    constructor(private http: HttpClient, private datePipe: DatePipe) {
        
    }
    getLists(): Promise<any> {
        let url: string = this.BASE_URL2;
        return this.http.get(url,{headers: this.headers}).toPromise();
    }

    getListType(): Promise<any> {
        let url: string = 'http://localhost:5000/api/listtype';
        return this.http.get(url,{headers: this.headers}).toPromise();
    }

    getEvents(event: Event): Promise<any> {
        let url: string = this.BASE_URL;
        return this.http.get(url,{headers: this.headers}).toPromise();
    }

    updateEvent(event: Event): Promise<any> {
        let url: string = `${this.BASE_URL}/${event.id}`;
        return this.http.put(url,event,{headers: this.headers}).toPromise();
    }

    deleteEvent(id): Promise<any> {
        let url: string = `${this.BASE_URL}/${id}`;
        return this.http.delete(url,{headers: this.headers}).toPromise();
    }

    insertEvent(event: Event): Promise<any> {
        let url: string = this.BASE_URL;
        console.log("hello troi oi " + event.start_date)
        
      
        return this.http.post(url,event,{headers: this.headers}).toPromise();
    }

}