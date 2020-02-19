import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Event} from '../Models/event';
import {List_User} from '../Models/list_user';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class CustomCalendarService {
    private BASE_URL: string = 'http://localhost:5000/api/custom-calendar/events';
    private BASE_URL2: string = 'http://localhost:5000/api/listtype';
    private headers: HttpHeaders = new HttpHeaders({'Content-Type': 'application/json'});
    
    constructor(private http: HttpClient) {
        
    }
    list_find(list_user: List_User): Promise<any> {
        let url: string =  'http://localhost:5000/api/custom-calendar/search'
        return this.http.post(url,list_user,{headers: this.headers}).toPromise();
    }

    getListUser(): Promise<any> {
        let url: string = 'http://localhost:5000/api/custom-calendar/list-user'
        return this.http.get(url,{headers: this.headers}).toPromise();
    }

    getListType(): Promise<any> {
        let url: string = this.BASE_URL2
        return this.http.get(url,{headers: this.headers}).toPromise();
    }

    getEvents(event: Event): Promise<any> {
        let url: string = this.BASE_URL;
        return this.http.get(url,{headers: this.headers}).toPromise();
    }

    updateEvent(event: Event,id): Promise<any> {
        let url: string = `${this.BASE_URL}/${id}`;
        return this.http.put(url,event,{headers: this.headers}).toPromise();
    }

    deleteEvent(id): Promise<any> {
        let url: string = `${this.BASE_URL}/${id}`;
        return this.http.delete(url,{headers: this.headers}).toPromise();
    }

    insertEvent(event: Event): Promise<any> {
        let url: string = this.BASE_URL;
        return this.http.post(url,event,{headers: this.headers}).toPromise();
    }



}