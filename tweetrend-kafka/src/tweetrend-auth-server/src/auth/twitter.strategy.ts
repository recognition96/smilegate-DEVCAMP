import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { PassportStrategy } from '@nestjs/passport';
import { Strategy } from 'passport-twitter';

import { UserRole } from '../user/user.entity';
import { UserService } from '../user/user.service';

import { AuthService } from './auth.service';

@Injectable()
export class TwitterStrategy extends PassportStrategy(Strategy, 'twitter') {
  constructor(
    private readonly config: ConfigService,
    private readonly userService: UserService,
    private readonly authService: AuthService,
  ) {
    super({
      consumerKey: config.get('TWITTER_CONSUMER_KEY'),
      consumerSecret: config.get('TWITTER_CONSUMER_SECRET'),
      callbackURL: '/auth/twitter/callback',
    });
  }

  async validate(
    token: string,
    tokenSecret: string,
    profile: any,
    done: (err: any, user: any, info?: any) => void,
  ): Promise<any> {
    const {
      id: provider_id,
      username,
      displayName,
      provider,
      photos,
    } = profile;
    const [{ value: profile_image_url }] = photos;

    const user =
      (await this.userService.getUserByUsername(username)) ||
      (await this.userService.createUser({
        provider_id,
        name: displayName,
        username,
        profile_image_url,
        provider,
      }));

    if (user.id === 1) {
      await this.userService.updateUserById(1, {
        role: UserRole.ADMIN,
      });
    }

    await this.userService.updateUserById(user.id, {
      access_token: token,
      access_token_secret: tokenSecret,
      accessed_at: new Date(),
    });

    const userData = {
      id: provider_id,
      name: user.name,
      username: user.username,
      profile_image_url: user.profile_image_url,
      provider: user.provider,
    };

    const jwt = this.authService.sign(userData);

    done(null, jwt);
  }
}
