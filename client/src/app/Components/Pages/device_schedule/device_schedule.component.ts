import {Component, ElementRef, OnInit, ViewChild, ViewEncapsulation } from "@angular/core";
import "dhtmlx-scheduler";
import {DeviceCalendarService} from '../../../Services/devicecalendar.service';
import { Router } from '@angular/router';
import {User} from '../../../Models/user'
import {Event} from '../../../Models/event'
import {EventService} from '../../../Services/schedule.module'
import '../../../../../node_modules/dhtmlx-scheduler/codebase/ext/dhtmlxscheduler_multiselect.js'
import '../../../../../node_modules/dhtmlx-scheduler/codebase/ext/dhtmlxscheduler_editors.js'
declare let dhtmlx: any;
declare var test: any;
// declare let scheduler: any;
@Component({
    encapsulation: ViewEncapsulation.None,
    selector: "device_schedule",
    styleUrls: ['device_schedule.component.css'],
    templateUrl: 'device_schedule.component.html',
    providers: [DeviceCalendarService]
})

export class DeviceScheduleComponent implements OnInit {
    event: Event = new Event();
    constructor(private router: Router, private devicecalendar: DeviceCalendarService) {
    }
    
    @ViewChild("device_schedule", {static:true}) schedulerContainer: ElementRef;
    
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
        var format = scheduler.date.date_to_str("%Y-%m-%d %H:%i");
        scheduler.templates.tooltip_text = function(start,end,event) {
            
            return "<b>Name:</b> "+event.name_device+"<br/><b>Event:</b> "+event.text+"<br/><b>Start date:</b> "+
            format(start)+"<br/><b>End date:</b> "+format(end);
        };

        scheduler.config.lightbox.sections = [
            { name:"Content", height:50, map_to:"text", type:"textarea", focus:true },
            { name:"Invite", height:30, map_to:"users", type:'multiselect', options: scheduler.serverList("users"),vertical: false }
        ];

        this.devicecalendar.getListType().then((array)=>{
            for(var i =0 ; i< array.length;i++){
                console.log(array[i].prefix)
                scheduler.config.lightbox.sections.push({ name:array[i].name, height:30, map_to:array[i].prefix, type:'multiselect', options: scheduler.serverList(array[i].prefix), vertical: false });
            }
        }).catch((err)=>{
            console.log(err);
            
        })

    
        scheduler.config.lightbox.sections.push({ name:"time", height:72, type:"time", map_to:"auto"})
        scheduler.init(this.schedulerContainer.nativeElement, new Date(2020, 2, 4));
        
        // doi id su kien mac dinh thanh id su kien theo database
        scheduler.attachEvent("onEventAdded", (id, ev) => {
            console.log(ev)
            this.devicecalendar.insertEvent(ev)
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
            this.devicecalendar.updateEvent(ev,id).then((response)=>{
                if (response.action == 'success') {
                    scheduler.clearAll();
                    this.devicecalendar.getEvents(this.event)
                    .then((event) => {
                        scheduler.parse(event, "json");
                        this.notif_responce(response.message);
                    })
                    .catch((err) => {
                        this.notif_responce("refresh error");
                    console.log(err);
                    });
                }
                else{
                    scheduler.clearAll();
                    this.devicecalendar.getEvents(this.event)
                    .then((event) => {
                        scheduler.parse(event, "json");
                        this.notif_responce(response.message);
                    })
                    .catch((err) => {
                        this.notif_responce("refresh error");
                    console.log(err);
                    });
                 
                }
            })
        });

        scheduler.attachEvent("onEventDeleted", (id,ev) => {
            this.devicecalendar.deleteEvent(id).then((response=>{
                if (response.action == 'success') {
                    
                    this.notif_responce(response.message);
                }
                else{
                    
                    this.notif_responce(response.message);
                }
            }))
        });
       
        this.devicecalendar.getEvents(this.event)
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