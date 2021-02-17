import {
  IsBoolean,
  IsDate,
  IsEmail,
  IsEnum,
  IsString,
  IsUrl,
} from 'class-validator';
import { BaseEntity, Column, Entity, PrimaryGeneratedColumn } from 'typeorm';

export enum UserRole {
  ADMIN = 'admin',
  USER = 'user',
}

@Entity()
export class User extends BaseEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  provider_id: string;

  @Column({
    nullable: true,
  })
  @IsEmail()
  email: string;

  @Column()
  @IsString()
  name: string;

  @Column()
  @IsString()
  username: string;

  @Column({
    nullable: true,
  })
  @IsUrl()
  profile_image_url: string;

  @Column({
    nullable: true,
  })
  @IsString()
  access_token: string;

  @Column({
    nullable: true,
  })
  @IsString()
  access_token_secret: string;

  @Column()
  provider: string;

  @Column({
    type: 'enum',
    enum: UserRole,
    default: UserRole.USER,
  })
  @IsEnum(UserRole)
  role: UserRole;

  @Column({ default: true })
  @IsBoolean()
  is_active: boolean;

  @Column({ default: false })
  @IsBoolean()
  is_locked: boolean;

  @Column({
    type: 'datetime',
    default: () => 'CURRENT_TIMESTAMP',
  })
  @IsDate()
  created_at: Date;

  @Column({
    type: 'datetime',
    default: () => 'CURRENT_TIMESTAMP',
    onUpdate: 'CURRENT_TIMESTAMP',
  })
  @IsDate()
  updated_at: Date;

  @Column({
    type: 'datetime',
    default: () => 'CURRENT_TIMESTAMP',
  })
  @IsDate()
  accessed_at: Date;
}
