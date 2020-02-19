import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {CustomCalendarService} from '../../../Services/customcalendar.service';
import * as jquery from 'jquery';

@Component({
  selector: 'navbar',
  templateUrl: 'nav.component.html',
  styleUrls: ['nav.component.css'],
  providers: [CustomCalendarService]
})
export class NavbarComponent {
  constructor(private router: Router, private customcalendar: CustomCalendarService) {}
  listUser = [];
  ngOnInit() {
    this.customcalendar.getListUser().then((array)=>{
      this.listUser = array
      jquery(".mySelect").select2({
        data: array,
        placeholder: "Select",
        allowClear: false,
        minimumResultsForSearch: 5
        });
    }).catch((err)=>{
      console.log(err);
    })
  }
  
  searchUser(){
    var data = jquery(".mySelect").val()
    console.log(data)
    localStorage.setItem('list_user', data.toString());
    window.location.href = '/custom'
  }

  logoutUser(){
    //or
    //remove an key from local storage
    localStorage.removeItem('token');
    this.router.navigateByUrl('/login');
    //things that you want to do for logout
}
}