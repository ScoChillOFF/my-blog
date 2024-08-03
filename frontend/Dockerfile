FROM node:lts-alpine

WORKDIR /app

COPY ./my_blog/package.json .

RUN yarn install

COPY ./my_blog .

CMD ["yarn", "dev"]