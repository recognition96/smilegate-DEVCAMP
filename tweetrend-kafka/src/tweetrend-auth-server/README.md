# TweeTrend Auth Server

| Area               | Tech Stack                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Backend            | ![](https://img.shields.io/badge/Typescript-blue?color=007ACC&longCache=true&logo=Typescript&logoColor=white) ![](https://img.shields.io/badge/NestJS-red?&color=E0234E&longCache=true&logo=NestJS) ![](https://img.shields.io/badge/TypeORM-red?&longCache=true&) ![](https://img.shields.io/badge/MySQL-gray?longCache=true&logo=mysql) ![](https://img.shields.io/badge/Sign_In_with_Twitter-white?color=1DA1F2&longCache=true&logo=twitter&logoColor=white) ![](https://img.shields.io/badge/JWT-darkgray?longCache=true&logo=JSON-Web-Tokens&logoColor=white) |
| Linter & Formatter | ![](https://img.shields.io/badge/Prettier-white?color=1E2B33&longCache=true&logo=Prettier) ![](https://img.shields.io/badge/ESLint-white?color=453ABC&longCache=true&logo=ESlint) ![](https://img.shields.io/badge/🐶_Husky-Green?longCache=true&logo=Husky)                                                                                                                                                                                                                                                                                                       |

## Description

[Nest](https://github.com/nestjs/nest) framework TypeScript starter repository.

## 🏃‍ Quick Start

**1. ⬇️ Clone Project**

```bash
git clone http://stove-developers-gitlab.sginfra.net/stove-dev-camp/bigsmile/tweetrend-auth-server.git
```

**2. ⚙️ Configure Environment Variables**

Create `.env` file in root directory.

> ☝️ Also, you can manage development and testing as different env files. `.env.development` `.env.test`

[.env.example](/.env.sample)

**3. Register Twitter App**

To use social login, you need to register the app on Twitter and write the callback URL.

**4. 📦 Install Dependencies**

```bash
yarn install
# or
# npm install
```

**5. Create Database**

[create-user.sql](docs/create-user.sql)

**6. 🎉 Start**

```bash
# development
yarn start
# or
# npm run start

# watch mode
yarn start:dev
# or
# yarn run start:dev

# production mode
yarn start:prod
# or
# yarn run start:prod
```

**7. 🛠 Build**

```bash
yarn build
# or
# npm run build
```

## License

[MIT](/LICENSE) © [younho9](https://github.com/younho9)
