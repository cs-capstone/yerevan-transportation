import {Component} from '@angular/core';
import {PolylineManager} from "@agm/core";
import {ArrayType} from "@angular/compiler";

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.css'],
})
export class AppComponent {
  centerLat: number = 40.197814;
  centerLng: number = 44.493663;
  showInfo: boolean = false;
  routePairs: Array<any> = null;
  path: any = null;

  constructor(_polylineManager: PolylineManager) {

  }

  drawRoute(data) {
    this.path = data.path.map(s => ({
        ...s,
        lat: +s.lat,
        lng: +s.lng
      }));

    this.routePairs = this.path.reduce((acc, current, index, self) => {
      let dest = self[index + 1];
      acc.push({
        src: current,
        dest: dest,
        transport: dest ? data.transport[dest.id] : null
      });
        return acc;
    }, []);

    this.showInfo = true;
  }

}
