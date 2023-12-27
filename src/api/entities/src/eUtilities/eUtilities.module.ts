import { Module } from '@nestjs/common';
import { UtilitiesService } from './eUtilities.service';
import { UtilitiesController } from './eUtilities.controller';

@Module({
  providers: [UtilitiesService],
  controllers: [UtilitiesController],
})
export class UtilitiesModule {}