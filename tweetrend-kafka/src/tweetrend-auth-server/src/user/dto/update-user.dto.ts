import {
  IsBoolean,
  IsDate,
  IsEmail,
  IsEnum,
  IsString,
  IsUrl,
} from 'class-validator';

import { UserRole } from '../user.entity';

export class UpdateUserDto {
  @IsEmail()
  readonly provider_id?: string;

  @IsEmail()
  readonly email?: string;

  @IsString()
  readonly name?: string;

  @IsString()
  readonly username?: string;

  @IsUrl()
  readonly profile_image_url?: string;

  @IsString()
  access_token?: string;

  @IsString()
  access_token_secret?: string;

  @IsString()
  readonly provider?: string;

  @IsEnum(UserRole)
  readonly role?: UserRole;

  @IsBoolean()
  readonly is_active?: boolean;

  @IsBoolean()
  readonly is_locked?: boolean;

  @IsDate()
  readonly updated_at?: Date;

  @IsDate()
  readonly accessed_at?: Date;
}
