import {Component, ElementRef, OnInit, ViewChild, ViewEncapsulation } from "@angular/core";
import "dhtmlx-scheduler";
import {DatePipe} from '@angular/common'
import {MyCalendarService} from '../../../Services/mycalendar.service';
import { Router } from '@angular/router';
import {User} from '../../../Models/user'
import {Event} from '../../../Models/event'
import {EventService} from '../../../Services/schedule.module'
import '../../../../../node_modules/dhtmlx-scheduler/codebase/ext/dhtmlxscheduler_multiselect.js'
import '../../../../../node_modules/dhtmlx-scheduler/codebase/ext/dhtmlxscheduler_editors.js'
declare let dhtmlx: any;
// declare let scheduler: any;
@Component({
    encapsulation: ViewEncapsulation.None,
    selector: "schedule",
    styleUrls: ['schedule.component.css'],
    templateUrl: 'schedule.component.html',
    providers: [ MyCalendarService, DatePipe]
})

export class ScheduleComponent implements OnInit {
    event: Event = new Event();
    constructor(private router: Router, private mycalendar: MyCalendarService,public datePipe: DatePipe) {
    }
    
    @ViewChild("scheduler_here", {static:true}) schedulerContainer: ElementRef;
    
    ngOnInit() {
        var date = new Date();
        console.log(this.datePipe.transform(date,"yyyy-MM-dd")); //
        
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
            { name:"Invite", height:40, map_to:"users", type:'multiselect', options: scheduler.serverList("users"), vertical: false },
            { name:"Devices", height:72, map_to:"devices", type:'multiselect', options: scheduler.serverList("devices"), vertical: false },
            { name:"time", height:72, type:"time", map_to:"auto"}
        ];

        scheduler.init(this.schedulerContainer.nativeElement, new Date(2020, 2, 4));
        
        // doi id su kien mac dinh thanh id su kien theo database
        scheduler.attachEvent("onEventAdded", (id, ev) => {
            console.log(ev)
            this.datePipe.transform(ev.start_date,"yyyy-MM-dd")
            this.mycalendar.insertEvent(ev)
                .then((response)=> {
                    if (response.id != id) {
                        scheduler.changeEventId(id, response.id);
                    }
                })
        });

        scheduler.attachEvent("onEventChanged", (id, ev) => {
            console.log(ev);
            this.mycalendar.updateEvent(ev);
        });

        // scheduler.attachEvent("onConfirmedBeforeEventDelete", function(id,e){
        //     this.mycalendar.deleteEvent(id).then((response)=>{
        //         if (response.action == 'deleted'){
        //             scheduler.deleteEvent(id);
        //         }

        //     })
        //     return true;
        // });


        scheduler.attachEvent("onBeforeEventDelete", (id) => {
            this.mycalendar.deleteEvent(id).then(()=>{
                this.xuatthongbao();
                return true;
            }).catch((err)=>{
                this.baoloi();
                console.log(err);
                return false;
            })
        })
       
        this.mycalendar.getEvents(this.event)
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