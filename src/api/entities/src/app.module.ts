import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { CarsModule } from './cars/cars.module';
import { CafvsModule } from './cafvs/cafvs.module';
import { UtilitiesModule } from './eUtilities/eUtilities.module';


@Module({
  imports: [CarsModule, CafvsModule, UtilitiesModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
