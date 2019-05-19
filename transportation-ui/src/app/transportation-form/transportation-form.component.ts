import {Component, EventEmitter, OnInit, Output} from "@angular/core";
import {TransportationService} from "../services/transportation.service";
import {Street} from "../models/street";
import {Station} from "../models/station";


@Component({
  selector: 'app-transportation-form',
  templateUrl: './transportation-form.component.html',
  styleUrls: ['./transportation-form.component.css']
})
export class TransportationFormComponent implements OnInit {
  streets: Street[];

  fromStation: Station;
  toStation: Station;

  criterias: any[] = ['minimum transfers', 'shortest path'];
  criteria: string = '';

  @Output() onPathResponse: EventEmitter<any> = new EventEmitter<any>();

  isReady: boolean = false;


  constructor(private transportationService: TransportationService) {
  }

  async ngOnInit() {
    this.streets = await this.transportationService.getStreets();
    this.isReady = true;

  }

  setStation(fromTo, station) {
    this[`${fromTo}Station`] = station;
  }

  submit() {
    if (this.fromStation && this.toStation && this.criteria) {
      this.transportationService.getShortestPath(this).then(data => {
        if (this.criteria === 'shortest path') {
          this.onPathResponse.emit(data[0]);
        } else {
          this.onPathResponse.emit(data);
        }
      });
    }
  }

}
