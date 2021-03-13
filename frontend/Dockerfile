FROM node:14 as build-stage

WORKDIR /app

COPY package*.json ./
RUN npm install
COPY . .

ARG FRONTEND_ENV=production
RUN echo "\nFRONTEND_ENV = $FRONTEND_ENV\n"
ENV VUE_APP_ENV=${FRONTEND_ENV}

RUN npm run build

COPY ./nginx.conf /nginx.conf

# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx

COPY --from=build-stage /app/dist/ /usr/share/nginx/html
COPY --from=build-stage /nginx.conf /etc/nginx/conf.d/default.conf
# COPY ./nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
CMD ["nginx", "-g", "daemon off;"]
