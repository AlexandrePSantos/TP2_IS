import { Injectable } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class CarsService {
    private prisma = new PrismaClient();

    async findAll({skip = 0, take = 10}: 
        { skip?: number; take?: number } = {}): Promise<any[]> {
        return this.prisma.car.findMany({
            skip,
            take,
        });
    }

    async getPageCount({size = 10}): Promise<any> {
        return Math.ceil((await this.prisma.car.count()) / size);
    }

    async removeCar(id: string): Promise<any> {
        return this.prisma.car.delete({
            where: { id }
        });
    }

    // async update(id: string, field: string, value: number): Promise<any> {
    //     return this.prisma.car.update({
    //         where: { id },
    //         data: { [field]: value }
    //     });
    // }

    // async createCar({ maker, model, year, range, type, location }): Promise<any> {
    //     return this.prisma.car.create({
    //         data: { maker, model, year, range, type, location }
    //     });
    // }
}
