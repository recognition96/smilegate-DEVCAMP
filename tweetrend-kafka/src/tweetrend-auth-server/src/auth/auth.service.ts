import { Injectable } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';

import { SignUserDto } from './dto/sign-user.dto';

@Injectable()
export class AuthService {
  constructor(private readonly jwtService: JwtService) {}

  sign(userData: SignUserDto) {
    return this.jwtService.sign(userData);
  }
}
