#builder
FROM node:lts-alpine as builder

WORKDIR /usr/src/app

COPY --from=frontend_src . .
RUN npm ci
RUN npm run build

#final

FROM nginx:alpine
COPY default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /usr/src/app/build /usr/share/nginx/html

