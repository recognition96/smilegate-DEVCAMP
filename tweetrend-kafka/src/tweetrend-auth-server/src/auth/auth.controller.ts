import {
  Controller,
  Get,
  HttpStatus,
  Req,
  Res,
  UseGuards,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { AuthGuard } from '@nestjs/passport';
import { Request, Response } from 'express';

@Controller('auth')
export class AuthController {
  constructor(private readonly config: ConfigService) {}

  @UseGuards(AuthGuard('twitter'))
  @Get('twitter')
  async twitterLogin(): Promise<any> {
    return HttpStatus.OK;
  }

  @UseGuards(AuthGuard('twitter'))
  @Get('twitter/callback')
  async twitterLoginRedirect(
    @Req() req: Request,
    @Res() res: Response,
  ): Promise<any> {
    res.redirect(`${this.config.get('CLIENT_URL')}/verified?token=${req.user}`);
  }
}
