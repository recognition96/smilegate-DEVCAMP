import { IsEmail, IsString, IsUrl } from 'class-validator';

export class SignUserDto {
  @IsEmail()
  readonly id?: string;

  @IsEmail()
  readonly email?: string;

  @IsString()
  readonly name?: string;

  @IsString()
  readonly username?: string;

  @IsUrl()
  readonly profile_image_url?: string;

  @IsString()
  readonly provider?: string;
}
