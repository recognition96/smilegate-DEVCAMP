import { IsEmail, IsOptional, IsString, IsUrl } from 'class-validator';

export class CreateUserDto {
  @IsString()
  readonly provider_id: string;

  @IsEmail()
  @IsOptional()
  readonly email?: string;

  @IsString()
  readonly name: string;

  @IsString()
  readonly username: string;

  @IsUrl()
  @IsOptional()
  readonly profile_image_url?: string;

  @IsString()
  readonly provider: string;
}
