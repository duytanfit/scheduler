import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from './auth.service';
import {HttpClient, HttpHeaders} from '@angular/common/http';
@Injectable()
export class EnsureAuthenticated implements CanActivate {
  constructor(private auth: AuthService, private router: Router, private http: HttpClient) {}
  private headers: HttpHeaders = new HttpHeaders({'Content-Type': 'application/json'});
  canActivate(): boolean {
    if (localStorage.getItem('token')) {
      return true;
    }
    else {
      this.router.navigateByUrl('/login');
      return false;
    }
  }

  getCurrentUser(): Promise<any> {
    let url: string = ""
    return this.http.get(url,{headers: this.headers}).toPromise();
  }
}