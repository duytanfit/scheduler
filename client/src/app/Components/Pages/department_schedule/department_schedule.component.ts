import {Component, ElementRef, OnInit, ViewChild, ViewEncapsulation } from "@angular/core";
import "dhtmlx-scheduler";
import {DepartmentCalendarService} from '../../../Services/departmentcalendar.service';
import { Router } from '@angular/router';
import {User} from '../../../Models/user'
import {Event} from '../../../Models/event'
import {EventService} from '../../../Services/schedule.module'
import '../../../../../node_modules/dhtmlx-scheduler/codebase/ext/dhtmlxscheduler_multiselect.js'
import '../../../../../node_modules/dhtmlx-scheduler/codebase/ext/dhtmlxscheduler_editors.js'
import '../../../../../node_modules/dhtmlx-scheduler/codebase/ext/dhtmlxscheduler_tooltip.js'
declare let dhtmlx: any;

// declare let scheduler: any;
@Component({
    encapsulation: ViewEncapsulation.None,
    selector: "department_schedule",
    styleUrls: ['department_schedule.component.css'],
    templateUrl: 'department_schedule.component.html',
    providers: [DepartmentCalendarService]
})

export class DepartmentScheduleComponent implements OnInit {
    event: Event = new Event();
    constructor(private router: Router, private departmentcalendar: DepartmentCalendarService) {
    }
    
    @ViewChild("department_schedule", {static:true}) schedulerContainer: ElementRef;
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
            return "<b>Own:</b> "+event.first_name+"<br/><b>Event:</b> "+event.text+"<br/><b>Start date:</b> "+
                format(start)+"<br/><b>End date:</b> "+format(end);
        };

        
        scheduler.config.lightbox.sections = [
            { name:"Content", height:50, map_to:"text", type:"textarea", focus:true },
            { name:"Invite", height:30, map_to:"users", type:'multiselect', options: scheduler.serverList("users"),vertical: false }
        ];

        this.departmentcalendar.getListType().then((array)=>{
            for(var i =0 ; i< array.length;i++){
                console.log(array[i].prefix)
                scheduler.config.lightbox.sections.push({ name:array[i].name, height:30, map_to:array[i].prefix, type:'multiselect', options: scheduler.serverList(array[i].prefix), vertical: false });
            }
        }).catch((err)=>{
            console.log(err);
            
        })
        scheduler.config.lightbox.sections.push({ name:"time", height:72, type:"time", map_to:"auto"})
        scheduler.init(this.schedulerContainer.nativeElement, new Date(2020, 2, 4));
        
        scheduler.attachEvent("onEventAdded", (id, ev) => {
            console.log(ev)
            this.departmentcalendar.insertEvent(ev)
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
            this.departmentcalendar.updateEvent(ev,id).then((response)=>{
                if (response.action == 'success') {
                    this.notif_responce(response.message);
                }
                else{
                    
                    this.departmentcalendar.getEvents(this.event)
                    .then((event) => {
                        scheduler.parse(event, "json");
                        this.notif_responce(response.message);
                    })
                    .catch((err) => {
                    this.notif_responce("Refresh error")
                    });
                    
                }
            })
        });

        scheduler.attachEvent("onEventDeleted", (id,ev) => {
            this.departmentcalendar.deleteEvent(id).then((response=>{
                if (response.action == 'success') {
                    this.notif_responce(response.message);
                }
                else{
                    this.notif_responce(response.message);
                }
            }))
        });
       
        this.departmentcalendar.getEvents(this.event)
            .then((event) => {
                console.log(event)
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