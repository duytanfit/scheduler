import {Component, ElementRef, OnInit, ViewChild, ViewEncapsulation } from "@angular/core";
import "dhtmlx-scheduler";
import {CustomCalendarService} from '../../../Services/customcalendar.service';
import { Router } from '@angular/router';
import {User} from '../../../Models/user'
import {List_User} from '../../../Models/list_user'
import {Event} from '../../../Models/event'
import {EventService} from '../../../Services/schedule.module'
import '../../../../../node_modules/dhtmlx-scheduler/codebase/ext/dhtmlxscheduler_multiselect.js'
import '../../../../../node_modules/dhtmlx-scheduler/codebase/ext/dhtmlxscheduler_editors.js'
declare let dhtmlx: any;

// declare let scheduler: any;
@Component({
    encapsulation: ViewEncapsulation.None,
    selector: "custom_schedule",
    styleUrls: ['custom_schedule.component.css'],
    templateUrl: 'custom_schedule.component.html',
    providers: [CustomCalendarService]
})

export class CustomScheduleComponent implements OnInit {
    event: Event = new Event();
    list_user: List_User = new List_User();
    constructor(private router: Router, private customcalendar: CustomCalendarService) {
    }
    
    @ViewChild("custom_schedule", {static:true}) schedulerContainer: ElementRef;
    
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

        this.customcalendar.getListType().then((array)=>{
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
        
        scheduler.attachEvent("onEventAdded", (id, ev) => {
            console.log(ev)
            this.customcalendar.insertEvent(ev)
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
            this.customcalendar.updateEvent(ev,id).then((response)=>{
                if (response.action == 'success') {
                   
                    this.notif_responce(response.message);
                }
                else{
                   
                    this.notif_responce(response.message);
                }
            })
        });

        scheduler.attachEvent("onEventDeleted", (id,ev) => {
            this.customcalendar.deleteEvent(id).then((response=>{
                if (response.action == 'success') {
                   
                    this.notif_responce(response.message);
                }
                else{
                   
                    this.notif_responce(response.message);
                }
            }))
        });
       
       this.list_user.list_user = localStorage.getItem('list_user');
        this.customcalendar.list_find(this.list_user)
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