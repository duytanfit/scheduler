import { Component } from '@angular/core';
import { Router } from '@angular/router';
@Component({
  selector: 'navbar',
  templateUrl: 'nav.component.html',
  styleUrls: ['nav.component.css']
})
export class NavbarComponent {
  constructor(private router: Router) {}
  logoutUser(){
        //or
    //remove an key from local storage
    localStorage.removeItem('token');
    this.router.navigateByUrl('/login');
    //things that you want to do for logout
}
}