import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-route-info',
  templateUrl: './route-info.component.html',
  styleUrls: ['./route-info.component.css']
})
export class RouteInfoComponent implements OnInit {

  @Input() pair: any = null;

  constructor() { }

  ngOnInit() {}

}
