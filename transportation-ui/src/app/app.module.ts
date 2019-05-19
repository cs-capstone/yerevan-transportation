import {BrowserModule} from "@angular/platform-browser";
import {NgModule} from "@angular/core";
import {CommonModule} from "@angular/common";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {AppComponent} from "./app.component";
import {AgmCoreModule, AgmPolyline, GoogleMapsAPIWrapper, MarkerManager, PolylineManager} from "@agm/core";
import { AgmDirectionModule } from 'agm-direction';
import {TransportationFormComponent} from "./transportation-form/transportation-form.component";
import {MatAutocompleteModule} from "@angular/material/autocomplete";
import {MatFormFieldModule, MatInputModule, MatOptionModule, MatSelectModule} from "@angular/material";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {TransportationService} from "./services/transportation.service";
import { HttpClientModule } from '@angular/common/http';
import { SelectStationComponent } from './select-station/select-station.component';
import { RouteInfoComponent } from './route-info/route-info.component';

@NgModule({
  imports: [
    BrowserModule,
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatAutocompleteModule,
    MatFormFieldModule,
    MatInputModule,
    MatOptionModule,
    MatSelectModule,
    BrowserAnimationsModule,
    HttpClientModule,
    AgmDirectionModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyBlJYPIV-z33FrC2Sd50YzHFaYa-jIOFUI'
    })
  ],
  providers: [TransportationService, PolylineManager, GoogleMapsAPIWrapper],
  declarations: [AppComponent, TransportationFormComponent, SelectStationComponent, RouteInfoComponent],
  bootstrap: [AppComponent]
})
export class AppModule {
}
