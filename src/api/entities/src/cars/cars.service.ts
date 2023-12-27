import { Injectable } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class CarsService {
    private prisma = new PrismaClient();

    async findAll(): Promise<any[]> {
        return this.prisma.car.findMany();
    }
}
