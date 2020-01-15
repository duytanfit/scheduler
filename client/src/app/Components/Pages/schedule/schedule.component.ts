import {Component, ElementRef, OnInit, ViewChild, ViewEncapsulation } from "@angular/core";
import "dhtmlx-scheduler";

import {Event} from '../../../Models/event'
import {EventService} from '../../../Services/schedule.module'


// declare let scheduler: any;
@Component({
    encapsulation: ViewEncapsulation.None,
    selector: "schedule",
    styleUrls: ['schedule.component.css'],
    templateUrl: 'schedule.component.html',
    providers: [ EventService ]
})

export class ScheduleComponent implements OnInit {
    @ViewChild("scheduler_here", {static:true}) schedulerContainer: ElementRef;
    constructor(private eventService: EventService) {}

    ngOnInit() {
        scheduler.config.full_day = true;
        scheduler.config.xml_date = '%Y-%m-%d %H:%i';      

        

			scheduler.config.lightbox.sections = [	
				{name:"description", height:50, map_to:"text", type:"textarea" , focus:true},
        
                {name:"type", height:30, map_to:"type", type:"select",  options:[
					{key:1, label:"Simple"},
					{key:2, label:"Complex"},
					{key:3, label:"Unknown"}
				]},
				{name:"time", height:72, type:"time", map_to:"auto"}	
            ];
            
        scheduler.init(this.schedulerContainer.nativeElement, new Date(2017, 8, 1));
        var events = [
            {id:1, text:"Meeting",   start_date:"2019-11-14 14:00",end_date:"2019-11-14 17:00"},
            {id:2, text:"Conference",start_date:"2019-11-13 12:00",end_date:"2019-11-13 19:00"},
            {id:3, text:"Interview", start_date:"2019-11-14 09:00",end_date:"2019-11-14 10:00"}
            ];
             
        // scheduler.parse(events)

        this.eventService.get().subscribe(data=>{
            console.log(data);
            scheduler.parse(data, "json");
        })
       
    }

}