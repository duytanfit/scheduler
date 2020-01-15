import {Component, ElementRef, OnInit, ViewChild, ViewEncapsulation } from "@angular/core";
import "dhtmlx-scheduler";
// declare let scheduler: any;
@Component({
    encapsulation: ViewEncapsulation.None,
    selector: "device_schedule",
    styleUrls: ['device_schedule.component.css'],
    templateUrl: 'device_schedule.component.html'
})

export class DeviceScheduleComponent implements OnInit {
    @ViewChild("scheduler_here", {static:true}) schedulerContainer: ElementRef;
   

    ngOnInit() {
       
        scheduler.init(this.schedulerContainer.nativeElement, new Date(2017, 8, 1));
        var events = [
            {id:1, text:"Meeting",   start_date:"2019-11-14 14:00",end_date:"2019-11-14 17:00"},
            {id:2, text:"Conference",start_date:"2019-11-13 12:00",end_date:"2019-11-13 19:00"},
            {id:3, text:"Interview", start_date:"2019-11-14 09:00",end_date:"2019-11-14 10:00"}
            ];
             
        scheduler.parse(events)
    }

}