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
    console.log(this.user)
    this.auth.login(this.user)
    .then((user) => {
      console.log(user.auth_token);
      localStorage.setItem('token', user.auth_token);
      this.router.navigateByUrl('/');
    })
    .catch((err) => {
      console.log(err);
    });
  }
}