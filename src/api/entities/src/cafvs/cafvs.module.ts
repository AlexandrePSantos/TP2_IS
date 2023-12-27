import { Module } from '@nestjs/common';
import { CafvsService } from './cafvs.service';
import { CafvsController } from './cafvs.controller';

@Module({
  providers: [CafvsService],
  controllers: [CafvsController],
})
export class CafvsModule {}