import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
// import { TeachersModule } from './teachers/teachers.module';
import { CarsModule } from './cars/cars.module';
import { LocationsModule } from './locations/locations.module';
import { CafvsModule } from './cafvs/cafvs.module';
import { UtilitiesModule } from './eUtilities/eUtilities.module';


@Module({
  // imports: [TeachersModule],
  imports: [CarsModule, LocationsModule, CafvsModule, UtilitiesModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
