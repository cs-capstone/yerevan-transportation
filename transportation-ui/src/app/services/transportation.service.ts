import {HttpClient} from "@angular/common/http";
import {Injectable} from "@angular/core";
import {Street} from "../models/street";
import {Station} from "../models/station";

@Injectable()
export class TransportationService {
  private BACK_END_URL = 'http://localhost:6543';

  constructor(private http: HttpClient) {

  }

  getStreets(): Promise<Street[]> {
    return this.http.get<Street[]>(`${this.BACK_END_URL}/streets`).toPromise();
  }

  getStations(streetId): Promise<Station[]> {
    return this.http.get<Station[]>(`${this.BACK_END_URL}/stations?street_id=${streetId}`).toPromise();
  }

  getShortestPath({ fromStation, toStation, criteria }) {
    let urls = {
      'minimum transfers': 'minimum_transfers',
      'shortest path': 'shortest_path'
    };

    let url = `${this.BACK_END_URL}/${urls[criteria]}?start_id=${fromStation.id}&end_id=${toStation.id}`;

    return this.http.get(url).toPromise();
  }

}
