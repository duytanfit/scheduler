import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {CommonModule} from '@angular/common'
import { FormsModule} from '@angular/forms';

import {ScheduleComponent} from './Components/Pages/schedule/schedule.component'
import {DepartmentScheduleComponent} from './Components/Pages/department_schedule/department_schedule.component'
import {DeviceScheduleComponent} from './Components/Pages/device_schedule/device_schedule.component'
import {CustomScheduleComponent} from './Components/Pages/custom_schedule/custom_schedule.component'
import {LoginComponent} from './Components/Pages/login/login.component'
import {DashboardComponent} from './Components/Pages/dashboard/dashboard.component'
import {ProfileComponent} from './Components/Pages/profile/profile.component'
import {StatusComponent} from './Components/Pages/status/status.component'

import { EnsureAuthenticated } from './Services/ensure-authenticated.service';
import { LoginRedirect } from './Services/login-redirect.service';
import { AuthService } from './Services/auth.service';
const routes: Routes = [
  {path:'schedule', component: ScheduleComponent, canActivate: [EnsureAuthenticated]},
  {path:'department', component: DepartmentScheduleComponent, canActivate: [EnsureAuthenticated]},
  {path:'device', component:DeviceScheduleComponent, canActivate: [EnsureAuthenticated]},
  {path:'custom', component:CustomScheduleComponent, canActivate: [EnsureAuthenticated]},
  {path:'dashboard', component: DashboardComponent},
  {path:'login', component: LoginComponent, canActivate: [LoginRedirect]},
  {path:'profile', component: ProfileComponent, canActivate: [EnsureAuthenticated]},
  {path:'status', component: StatusComponent, canActivate: [EnsureAuthenticated]},
  {path: '**', component:ScheduleComponent, canActivate: [EnsureAuthenticated]}
];

@NgModule({
  declarations: [
    ScheduleComponent,
    DepartmentScheduleComponent,
    DeviceScheduleComponent,
    CustomScheduleComponent,
    DashboardComponent,
    LoginComponent,
    ProfileComponent,
    StatusComponent
  ],
  imports: [
    RouterModule.forRoot(routes),
    CommonModule,
    FormsModule
  ],
  providers:[
    AuthService,
    EnsureAuthenticated,
    LoginRedirect
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
