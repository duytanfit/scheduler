import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Event} from '../Models/event';
import {HandleError} from '../Services/service-helper'
import {DatePipe} from '@angular/common'
import 'rxjs/add/operator/toPromise';
// export class ScheduleSevice{
//     constructor(private http: HttpClient){}

//     getSchedule(){
//         let options: 
//         {
//             headers: new HttpHeaders().set("Content-Type", "application/x-www-form-urlencoded")
//         }
//         return this.http.post("http://localhost:5000/api/scheudle",options);

//     }

// }
@Injectable()
export class EventService {
    private eventUrl = 'http://localhost:5000/api/events';
    private eventUrl2 = 'http://localhost:5000/api/events/users';
    constructor(private http: HttpClient) {}

    get(){
        return this.http.get(this.eventUrl)
    }

    get2(){
        return this.http.get(this.eventUrl2)
    }
}