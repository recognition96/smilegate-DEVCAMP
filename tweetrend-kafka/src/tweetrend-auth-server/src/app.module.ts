import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import * as Joi from 'joi';

import { AppController } from './app.controller';
import { AppService } from './app.service';
import { AuthModule } from './auth/auth.module';
import { DatabaseModule } from './db/database.module';
import { UserModule } from './user/user.module';

const ENV = process.env.NODE_ENV || 'development';

@Module({
  imports: [
    ConfigModule.forRoot({
      envFilePath: ENV === 'production' ? '.env' : `.env.${ENV}`,
      validationSchema: Joi.object({
        NODE_ENV: Joi.string()
          .valid('development', 'production', 'test')
          .default('development'),
        DB_HOST: Joi.string().required(),
        DB_PORT: Joi.number().required(),
        DB_USER: Joi.string().required(),
        DB_PASSWORD: Joi.string().required(),
        DB_NAME: Joi.string().required(),
        TWITTER_CONSUMER_KEY: Joi.string().required(),
        TWITTER_CONSUMER_SECRET: Joi.string().required(),
        FACEBOOK_CONSUMER_KEY: Joi.string().required(),
        FACEBOOK_CONSUMER_SECRET: Joi.string().required(),
        CLIENT_URL: Joi.string().required(),
        SESSION_SECRET: Joi.string().required(),
        JWT_SECRET: Joi.string().required(),
        JWT_EXPIRESIN: Joi.string().required(),
      }),
    }),
    DatabaseModule,
    UserModule,
    AuthModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
