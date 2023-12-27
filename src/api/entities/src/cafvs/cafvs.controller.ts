import { Controller, Get } from '@nestjs/common';
import { CafvsService } from './cafvs.service';

@Controller('cafvs')
export class CafvsController {
    constructor(private readonly cafvsService: CafvsService) {}

    @Get()
    findAll(): Promise<any[]> {
        return this.cafvsService.findAll();
    }
}
