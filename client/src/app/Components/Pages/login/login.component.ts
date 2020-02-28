import { Component, OnInit } from '@angular/core';
import {AuthService} from '../../../Services/auth.service';
import { Router } from '@angular/router';
import {User} from '../../../Models/user'

@Component({
  selector: 'login',
  templateUrl: 'login.component.html',
  styleUrls: ['login.component.css']
})

export class LoginComponent {
  user: User = new User();
  constructor(private router: Router, private auth: AuthService) {}
  onLogin(): void {
    this.auth.login(this.user)
    .then((data) => {
      console.log(data);
      if (data.status == 'success'){
        localStorage.setItem('token', data.access_token);
        this.router.navigateByUrl('/');
      }
      else{
        console.log(data.message)
        this.router.navigateByUrl('/login');
      }
    })
    .catch((err) => {
      console.log(err);
    });
  }
}