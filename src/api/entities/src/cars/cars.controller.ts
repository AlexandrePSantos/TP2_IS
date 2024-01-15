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

    // @Post("update")
    // async update(@Query('id') id: string, @Query('field') field: string, @Query('value') value: string) {
    //     return this.carsService.update(id, field, parseInt(value));
    // }
    
    // @Post("create")
    // async createCar(@Query('maker') maker: string, @Query('model') model: string, @Query('year') year: number, @Query('range') range: number, @Query('type') type: string, @Query('location') location: string) {
    //     return this.carsService.createCar({ maker, model, year, range, type, location });
    // }

}
