import { Controller, Get, Query } from '@nestjs/common';
import { CafvsService } from './cafvs.service';

@Controller('cafvs')
export class CafvsController {
    constructor(private readonly cafvsService: CafvsService) {}

    @Get()
    async findAll(@Query('page') page: number = 1) {
        const pageSize = 10;
        const skip = (page-1) * pageSize;
        
        return this.cafvsService.findAll({skip, take: pageSize});
    }

    @Get("pageCount")
    async pageCount(@Query('size') size: number = 10) {
        return this.cafvsService.getPageCount({size})
    }
}
