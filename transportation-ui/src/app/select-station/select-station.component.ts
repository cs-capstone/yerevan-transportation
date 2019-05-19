import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Street} from "../models/street";
import {TransportationService} from "../services/transportation.service";
import {Station} from "../models/station";
import {map, startWith} from "rxjs/operators";
import {Observable} from "rxjs/index";
import {FormControl} from "@angular/forms";


@Component({
  selector: 'app-select-station',
  templateUrl: './select-station.component.html',
  styleUrls: ['./select-station.component.css']
})
export class SelectStationComponent implements OnInit {
  @Input() streetsData;
  control: FormControl = new FormControl();
  stations: Station[] = [];
  filteredOptions: Observable<Street[]>;
  @Output() onStationSelected = new EventEmitter();

  constructor(private transportationService: TransportationService) {
  }

  ngOnInit() {
    this.filteredOptions = this.control.valueChanges
      .pipe(
        startWith(''),
        map(value => this._filter(value))
      );
  }

  private _filter(value): Street[] {
    const filterValue = value.name ? value.name : value;
    return this.streetsData.filter(s => s.name.toLowerCase().includes(filterValue.toLowerCase()));
  }

  async loadStations(street) {
    this.stations = await this.transportationService.getStations(street.id);
  }

  displayName = entity => entity && this.toTitleCase(entity.name);

  private toTitleCase = text => text.toLowerCase()
    .split(' ')
    .map(s => s.charAt(0).toUpperCase() + s.substring(1))
    .join(' ');

  emitStation(event) {
    this.onStationSelected.emit(event.value);
  }

}
