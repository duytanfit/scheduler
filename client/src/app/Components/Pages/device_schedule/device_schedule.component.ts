


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
    constructor(private router: Router, private departmentcalendar: DeviceCalendarService) {
    }
    
    @ViewChild("device_schedule", {static:true}) schedulerContainer: ElementRef;
    
    ngOnInit() {
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

        // for (var i =0 ; i < json.length;i++){
        //     scheduler.config.lightbox.sections.push({ name:array[i], height:72, map_to:array[i], type:'multiselect', options: scheduler.serverList(array[i]), script_url: this.mycalendar.getLists(), vertical: false });
        // }
        
        scheduler.config.lightbox.sections.push({ name:"time", height:72, type:"time", map_to:"auto"})
        scheduler.init(this.schedulerContainer.nativeElement, new Date(2020, 2, 4));
        
        // doi id su kien mac dinh thanh id su kien theo database
        scheduler.attachEvent("onEventAdded", (id, ev) => {
            console.log(ev)
            this.departmentcalendar.insertEvent(ev)
                .then((response)=> {
                    if (response.id != id) {
                        scheduler.changeEventId(id, response.tid);
                        // scheduler.clearAll();
                        // scheduler.load("http://localhost:5000/api/device-calendar/events");
                    }
                })
        });

        scheduler.attachEvent("onEventChanged", (id, ev) => {
            this.departmentcalendar.updateEvent(ev,id).then((response)=>{
                if(response.action == 'updated'){
                    // scheduler.clearAll();
                    // scheduler.load("http://localhost:5000/api/device-calendar/events");
                }
            })
        });

        scheduler.attachEvent("onEventDeleted", (id,ev) => {
            this.departmentcalendar.deleteEvent(id).then((response=>{
                if(response.action == 'deleted'){
                    // scheduler.clearAll();
                    // scheduler.load("http://localhost:5000/api/device-calendar/events");
                }
            }))
        });

        // scheduler.attachEvent("onBeforeEventDelete", (id) => {
        //     this.mycalendar.deleteEvent(id).then(()=>{
        //         this.xuatthongbao();
        //         return true;
        //     }).catch((err)=>{
        //         this.baoloi();
        //         console.log(err);
        //         return false;
        //     })
        // })
       
        this.departmentcalendar.getEvents(this.event)
            .then((event) => {
                scheduler.parse(event, "json");
        })
        .catch((err) => {
        console.log(err);
        });
    }

    private xuatthongbao(){
        dhtmlx.message({
            text: "Da xoa su kien",
            expire: 1000*3,
            position: "top"
    
        });
    }

    private baoloi(){
        dhtmlx.message({
            text: "Da xay ra loi",
            expire: 1000*3,
            position: "top"
    
        });
    }


}