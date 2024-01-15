import { Injectable } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class CafvsService {
  private prisma = new PrismaClient();

  async findAll({skip = 0, take = 10}: 
    { skip?: number; take?: number } = {}): Promise<any[]> {
    return this.prisma.cAFV.findMany({
      skip,
      take,
  });
  }

  async getPageCount({size = 10}): Promise<any> {
    return Math.ceil((await this.prisma.cAFV.count()) / size);
}
}