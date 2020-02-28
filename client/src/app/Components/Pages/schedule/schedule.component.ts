import {Component, ElementRef, OnInit, ViewChild, ViewEncapsulation } from "@angular/core";
import "dhtmlx-scheduler";
import {MyCalendarService} from '../../../Services/mycalendar.service';
import { Router } from '@angular/router';
import {Event} from '../../../Models/event'
import '../../../../../node_modules/dhtmlx-scheduler/codebase/ext/dhtmlxscheduler_multiselect.js'
import '../../../../../node_modules/dhtmlx-scheduler/codebase/ext/dhtmlxscheduler_editors.js'
declare let dhtmlx: any;
// declare let scheduler: any;
@Component({
    encapsulation: ViewEncapsulation.None,
    selector: "schedule",
    styleUrls: ['schedule.component.css'],
    templateUrl: 'schedule.component.html',
    providers: [ MyCalendarService]
})

export class ScheduleComponent implements OnInit {
    event: Event = new Event();
    constructor(private router: Router, private mycalendar: MyCalendarService) {}
    @ViewChild("scheduler_here", {static:true}) schedulerContainer: ElementRef;
    ngOnInit() {
        scheduler.clearAll();
        scheduler.config.prevent_cache = true;
		scheduler.config.first_hour=6;
		scheduler.config.limit_time_select = true;
		scheduler.config.details_on_create=true;
        scheduler.config.details_on_dblclick=true;
        scheduler.config.server_utc = false;
        scheduler.config.full_day = true;
        scheduler.config.xml_date = '%Y-%m-%d %H:%i';    
        scheduler.config.lightbox.sections = [
            { name:"Content", height:50, map_to:"text", type:"textarea", focus:true },
            { name:"Invite", height:30, map_to:"users", type:'multiselect', options: scheduler.serverList("users"),vertical: false },
            { name:"time", height:72, type:"time", map_to:"auto"}
        ];

        this.mycalendar.getListType().then((array)=>{
            for(var i =0 ; i< array.length;i++){
                console.log(array[i].prefix)
                scheduler.config.lightbox.sections.push({ name:array[i].name, height:30, map_to:array[i].prefix, type:'multiselect', options: scheduler.serverList(array[i].prefix), vertical: false });
            }
        }).catch((err)=>{
            console.log(err);
        })
        scheduler.init(this.schedulerContainer.nativeElement, new Date(2020, 2, 4));
        
        // doi id su kien mac dinh thanh id su kien theo database
        scheduler.attachEvent("onEventAdded", (id, ev) => {
            console.log(ev)
            this.mycalendar.insertEvent(ev)
                .then((response)=> {
                    if (response.action == 'success') {
                        scheduler.changeEventId(id, response.tid)
                        this.notif_responce(response.message);
                    }
                    else{
                        scheduler.deleteEvent(id);
                        this.notif_responce(response.message);
                    }
                })
        });
        scheduler.attachEvent("onEventChanged", (id, ev) => {
            console.log(ev);
            this.mycalendar.updateEvent(ev).then((response)=>{
                if (response.action == 'success') {
                   
                    this.notif_responce(response.message);
                }
                else{
                    
                    this.notif_responce(response.message);
                }
            })
        });
      

        scheduler.attachEvent("onEventDeleted", (id,ev) => {
            this.mycalendar.deleteEvent(id).then((response)=>{
                if (response.action == 'success') {
                   
                    this.notif_responce(response.message);
                }
                else{
                    
                    this.notif_responce(response.message);
                }
            })
        });
       
        this.mycalendar.getEvents(this.event)
            .then((event) => {
                scheduler.parse(event, "json");
        })
        .catch((err) => {
        console.log(err);
        });
    }

    private notif_responce(message){
        dhtmlx.message({ 
            text: message,
            expire: 1000*3,
            position: "top"
    
        });
    }

   


}