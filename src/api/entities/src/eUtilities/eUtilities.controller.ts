import { Controller, Get, Query } from '@nestjs/common';
import { UtilitiesService } from './eUtilities.service';

@Controller('utilities')
export class UtilitiesController {
    constructor(private readonly utilitiesService: UtilitiesService) {}

    @Get()
    async findAll(@Query('page') page: number = 1) {
        const pageSize = 10;
        const skip = (page-1) * pageSize;

        return this.utilitiesService.findAll({skip, take: pageSize});
    }

    @Get("pageCount")
    async pageCount(@Query('size') size: number = 10) {
        return this.utilitiesService.getPageCount({size})
    }
}