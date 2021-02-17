import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { DeleteResult, Repository, UpdateResult } from 'typeorm';

import { CreateUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';
import { User } from './user.entity';

@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User) private readonly userRepository: Repository<User>,
  ) {}

  async getUsers(): Promise<User[]> {
    return await this.userRepository.find();
  }

  async getUserById(id: number): Promise<User> {
    return await this.userRepository.findOne(id);
  }

  async getUserByUsername(username: string): Promise<User> {
    return await this.userRepository.findOne({ username });
  }

  async getUserByEmail(email: string): Promise<User> {
    return await this.userRepository.findOne({ email });
  }

  async createUser(user: CreateUserDto): Promise<User> {
    return await this.userRepository.save(user);
  }

  async remove(id: number): Promise<DeleteResult> {
    return await this.userRepository.delete(id);
  }

  async updateUserById(
    id: number,
    userData: UpdateUserDto,
  ): Promise<UpdateResult> {
    return await this.userRepository.update(id, userData);
  }
}
