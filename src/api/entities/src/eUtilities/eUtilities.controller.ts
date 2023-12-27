import { Controller, Get } from '@nestjs/common';
import { UtilitiesService } from './eUtilities.service';

@Controller('utilities')
export class UtilitiesController {
    constructor(private readonly utilitiesService: UtilitiesService) {}

    @Get()
    async findAll() {
        return this.utilitiesService.findAll();
    }
}