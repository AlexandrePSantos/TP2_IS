import { Controller, Get, Post, Query } from '@nestjs/common';
import { CarsService } from './cars.service';

@Controller('cars')
export class CarsController {
    constructor(private readonly carsService: CarsService) {}

    @Get()
    async findAll(@Query('page') page: number = 1) {
        const pageSize = 10;
        const skip = (page-1) * pageSize;

        return this.carsService.findAll({skip, take: pageSize});
    }

    @Get("pageCount")
    async pageCount(@Query('size') size: number = 10) {
        return this.carsService.getPageCount({size})
    }

    @Get("remove")
    async removeCar(@Query('id') id: string) {
        return this.carsService.removeCar(id);
    }
}
