import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {CommonModule} from '@angular/common'

import {ScheduleComponent} from './Components/Pages/schedule/schedule.component'
import {DepartmentScheduleComponent} from './Components/Pages/department_schedule/department_schedule.component'
import {DeviceScheduleComponent} from './Components/Pages/device_schedule/device_schedule.component'
import {LoginComponent} from './Components/Pages/login/login.component'
import {DashboardComponent} from './Components/Pages/dashboard/dashboard.component'
import {ProfileComponent} from './Components/Pages/profile/profile.component'

const routes: Routes = [
  {path:'schedule', component: ScheduleComponent},
  {path:'department', component: DepartmentScheduleComponent},
  {path:'device', component:DeviceScheduleComponent},
  {path:'dashboard', component: DashboardComponent},
  {path:'login', component: LoginComponent},
  {path:'profile', component: ProfileComponent},
  {path: '**', component:ScheduleComponent}
];

@NgModule({
  declarations: [
    ScheduleComponent,
    DepartmentScheduleComponent,
    DeviceScheduleComponent,
    DashboardComponent,
    LoginComponent,
    ProfileComponent
  ],
  imports: [
    RouterModule.forRoot(routes),
    CommonModule
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
